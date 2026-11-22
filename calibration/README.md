# Tyre degradation calibration

Run `python calibration/fit_tyre_degradation.py --csv PATH_TO_LAPS_CSV` to
reproduce the fit and held-out error report. The CSV used for the checked-in
report is a FastF1-derived export containing the 2023 Bahrain, British, and
Spanish races: [source file](https://github.com/KevalXD/CleanCurve/blob/main/raw_data/laps_raw.csv).
The script can also load sessions directly with FastF1 when its upstream timing
feed is available.

The fit uses Bahrain and Britain for training and Spain as a race-level holdout.
It keeps accurate, green-flag laps on dry compounds, drops pit entry/exit laps,
and removes laps slower than 107% of the event's fastest clean lap. Each stint's
lap times are differenced against its first retained lap, then corrected by a
fixed 0.055 seconds per tyre lap for fuel burn. A pooled least-squares slope is
fit through zero. The held-out MAE and RMSE compare later-stint lap-time changes
with the corrected tyre-age prediction.

This is an initial calibration, not a clean causal estimate: the fuel correction
is assumed, and track evolution, traffic, setup changes, and compound effects
remain in the residuals. On the one held-out race, the fitted 0.0313 s/lap rate
has higher error than the prior 0.08 s/lap rate. The config uses the measured
candidate, but the result does not establish that it generalizes better. More
race seasons and a model that separates fuel burn and track evolution are needed.
