"""Fit and evaluate tyre-age pace loss using FastF1 race lap data.

The response is each stint's lap time relative to its first clean green-flag
lap. This removes driver/stint pace offsets; slopes are pooled by compound.
Races are split before fitting so held-out events never affect coefficients.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import fastf1
import numpy as np


TRAIN_RACES = [(2023, "Bahrain"), (2023, "Great Britain")]
HELD_OUT_RACES = [(2023, "Spain")]
COMPOUNDS = ("SOFT", "MEDIUM", "HARD")
FUEL_BURN_SECONDS_PER_LAP = 0.055
CSV_EVENT_NAMES = {"Great Britain": "British"}


def load_race(year: int, event: str, csv_path: Path | None = None):
    if csv_path:
        import pandas as pd

        laps = pd.read_csv(csv_path)
        laps = laps.loc[
            (laps["Season"] == year)
            & (laps["GP"] == CSV_EVENT_NAMES.get(event, event))
            & (laps["SessionType"] == "R")
        ].copy()
        laps["LapSeconds"] = laps["LapTimeSec"]
    else:
        session = fastf1.get_session(year, event, "R")
        session.load(laps=True, telemetry=False, weather=False, messages=False)
        laps = session.laps.copy()
        laps["LapSeconds"] = laps["LapTime"].dt.total_seconds()
    # TrackStatus '1' means all clear. Pit entry/exit laps and inaccurate
    # timing records are not representative of tyre-age degradation.
    valid = (
        laps["LapSeconds"].notna()
        & laps["TyreLife"].notna()
        & laps["Compound"].isin(COMPOUNDS)
        & laps["TrackStatus"].fillna("").astype(str).eq("1")
        & laps["PitInTime"].isna()
        & laps["PitOutTime"].isna()
    )
    if "IsAccurate" in laps:
        valid &= laps["IsAccurate"].fillna(False)
    laps = laps.loc[valid].copy()
    if not laps.empty:
        fastest = laps.groupby("Season")["LapSeconds"].transform("min") if "Season" in laps else laps["LapSeconds"].min()
        laps = laps.loc[laps["LapSeconds"] <= 1.07 * fastest].copy()
    return laps


def stint_observations(laps):
    observations = []
    for (_, stint), group in laps.groupby(["Driver", "Stint"], sort=False):
        group = group.sort_values("LapNumber")
        if len(group) < 4:
            continue
        ages = group["TyreLife"].to_numpy(dtype=float)
        times = group["LapSeconds"].to_numpy(dtype=float)
        # TyreLife may start above one for a reused set, so use relative age.
        age_delta = ages - ages[0]
        time_delta = times - times[0]
        keep = (age_delta > 0) & np.isfinite(time_delta)
        if keep.sum() < 3:
            continue
        observations.append(
            {
                "compound": str(group["Compound"].iloc[0]),
                "age_delta": age_delta[keep],
                "time_delta": time_delta[keep],
            }
        )
    return observations


def fit_slope(observations):
    numerator = sum(
        float(x["age_delta"] @ (x["time_delta"] + FUEL_BURN_SECONDS_PER_LAP * x["age_delta"]))
        for x in observations
    )
    denominator = sum(float(x["age_delta"] @ x["age_delta"]) for x in observations)
    return numerator / denominator if denominator else 0.0


def score(observations, slope):
    errors = []
    for stint in observations:
        observed_tyre_delta = stint["time_delta"] + FUEL_BURN_SECONDS_PER_LAP * stint["age_delta"]
        errors.extend(observed_tyre_delta - slope * stint["age_delta"])
    values = np.asarray(errors, dtype=float)
    return {
        "laps": int(values.size),
        "mae_seconds": float(np.mean(np.abs(values))) if values.size else None,
        "rmse_seconds": float(np.sqrt(np.mean(values**2))) if values.size else None,
    }


def collect(races, csv_path=None):
    result = {}
    for year, event in races:
        key = f"{year} {event}"
        print(f"Loading {key}...", flush=True)
        result[key] = stint_observations(load_race(year, event, csv_path))
        print(f"  eligible stints: {len(result[key])}", flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, default=Path(".fastf1-cache"))
    parser.add_argument("--output", type=Path, default=Path("calibration/results.json"))
    parser.add_argument("--csv", type=Path, help="Use a CSV exported from FastF1 instead of downloading sessions")
    args = parser.parse_args()
    args.cache.mkdir(parents=True, exist_ok=True)
    if hasattr(fastf1.Cache, "configure"):
        fastf1.Cache.configure(cache_dir=str(args.cache))
    else:
        fastf1.Cache.enable_cache(str(args.cache))

    train = collect(TRAIN_RACES, args.csv)
    held_out = collect(HELD_OUT_RACES, args.csv)
    train_obs = [stint for event in train.values() for stint in event]
    if len(train_obs) < 20:
        raise SystemExit(f"Insufficient eligible training stints: {len(train_obs)}")
    slope = fit_slope(train_obs)
    held_out_obs = [stint for event in held_out.values() for stint in event]
    report = {
        "data_source": (
            "FastF1 race lap timing data" if not args.csv else
            "FastF1-derived lap CSV (KevalXD/CleanCurve raw_data/laps_raw.csv)"
        ),
        "data_source_url": "https://github.com/KevalXD/CleanCurve/blob/main/raw_data/laps_raw.csv",
        "train_races": list(train),
        "held_out_races": list(held_out),
        "training_stints": len(train_obs),
        "training_stints_by_race": {event: len(rows) for event, rows in train.items()},
        "held_out_stints_by_race": {event: len(rows) for event, rows in held_out.items()},
        "calibrated_seconds_per_tyre_lap": slope,
        "held_out_error": score(held_out_obs, slope),
        "held_out_error_by_race": {
            event: score(rows, slope) for event, rows in held_out.items()
        },
        "baseline_seconds_per_tyre_lap": 0.08,
        "baseline_held_out_error": score(held_out_obs, 0.08),
        "fuel_burn_correction_seconds_per_lap": FUEL_BURN_SECONDS_PER_LAP,
        "method": (
            "Ordinary least squares through origin on each clean stint's lap-time "
            "delta from its first clean green-flag lap, pooled across compounds. "
            "Held-out error is lap-weighted MAE/RMSE on later laps."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
