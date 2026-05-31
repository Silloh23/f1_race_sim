from simulator.config import RaceConfig
from simulator.race import RaceSimulator
from simulator.monte_carlo import MonteCarloEngine
import matplotlib.pyplot as plt
import numpy as np

config = RaceConfig()
sim = RaceSimulator(config)
mc = MonteCarloEngine(simulator=sim, n_runs=500)

one_stop = [25]
two_stop = [15,36]

base_1 = sim.run(one_stop)
base_2 = sim.run(two_stop)
monte_carlo_strat1 = mc.evaluate_strategy(one_stop)
monte_carlo_strat2 = mc.evaluate_strategy(two_stop)

print("------Base Strategy------")
print("One stop strategy time: ", base_1.total_time)
print("Two stop strategy time: ", base_2.total_time)
print("One stop pit stops: ", base_1.pit_stops)
print("Two stop pit stops: ", base_2.pit_stops)

print("------Monte Carlo Simulation------")
print("One stop mc strategy time: ", monte_carlo_strat1["mean_time"])
print("Two stop mc strategy time: ", monte_carlo_strat2["mean_time"])
print("One stop mc strategy std: ", monte_carlo_strat1["std_time"])
print("Two stop mc strategy std: ", monte_carlo_strat2["std_time"])

### ----- Base Strategy Plot -----

fig, axes = plt.subplots(2, 1, sharey=True, figsize=(15, 5))

### One Stop
laps1 = range(1, len(base_1.lap_times) + 1)

axes[0].plot(laps1, base_1.lap_times, label="Lap Times")

for pit_lap in base_1.pit_stops:
    axes[0].axvline(pit_lap + 1, linestyle="--", label="Pit Stop")

axes[0].set_title(f"One Stop Base Strat (Total Time={base_1.total_time})")
axes[0].set_xlabel("Lap")
axes[0].set_ylabel("Lap Times")
axes[0].legend()
axes[0].grid(True)
axes[0].set_ylim(80)

### Two Stop
laps2 = range(1, len(base_2.lap_times) + 1)

axes[1].plot(laps2, base_2.lap_times, label="Lap Times")

for pit_lap in base_2.pit_stops:
    axes[1].axvline(pit_lap + 1, linestyle="--", label="Pit Stop")

axes[1].set_title(f"Two Stop Base Strat (Total Time={base_2.total_time})")
axes[1].set_xlabel("Lap")
axes[1].set_ylabel("Lap Times")
axes[1].legend()
axes[1].grid(True)
axes[1].set_ylim(80)

plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt

times_1 = monte_carlo_strat1["all_results"]
times_2 = monte_carlo_strat2["all_results"]

fig, axes = plt.subplots(1, 2, figsize=(12, 10))

# -------------------
# Histogram Comparison
# -------------------
axes[0].hist(
    times_1,
    bins=30,
    alpha=0.6,
    label="One Stop"
)

axes[0].hist(
    times_2,
    bins=30,
    alpha=0.6,
    label="Two Stop"
)

axes[0].set_title("Monte Carlo Race Time Distribution")
axes[0].set_xlabel("Race Time (s)")
axes[0].set_ylabel("Frequency")
axes[0].legend()
axes[0].grid(True)

# -------------------
# Box Plot Comparison
# -------------------
axes[1].boxplot(
    [times_1, times_2],
    tick_labels=["One Stop", "Two Stop"]
)

axes[1].set_title("Monte Carlo Strategy Box Plot")
axes[1].set_ylabel("Race Time (s)")
axes[1].grid(True)

plt.tight_layout()
plt.show()