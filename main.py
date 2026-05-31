from simulator.config import RaceConfig
from simulator.race import RaceSimulator
import matplotlib.pyplot as plt
import numpy as np

config = RaceConfig()
sim = RaceSimulator(config)

one_stop = [25]
two_stop = [15,36]

base_strat = sim.run(one_stop)
result2 = sim.run(two_stop)

print("One stop strategy time: ", base_strat.total_time)
print("Two stop strategy time: ", result2.total_time)

print("One stop pit stops: ", base_strat.pit_stops)
print("Two stop pit stops: ", result2.pit_stops)


laps = range(1, len(base_strat.lap_times) + 1)
plt.figure(figsize=(12, 6))

plt.plot(
    laps,
    base_strat.lap_times,
    label="Lap Times"
)

for pit_lap in base_strat.pit_stops:
    plt.axvline(
        pit_lap + 1,
        linestyle = "--",
        label="Pit Stop"
    )
    
plt.title("One Stop Base Strat")
plt.xlabel("Lap")
plt.ylabel("Lap Times")
plt.legend()
plt.grid(True)
plt.ylim(80)

plt.show()