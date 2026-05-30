from simulator.config import RaceConfig
from simulator.race import RaceSimulator

config = RaceConfig()
sim = RaceSimulator(config)

one_stop = [25]
two_stop = [15,36]

result1 = sim.run(one_stop)
result2 = sim.run(two_stop)

print("One stop strategy time: ", result1.total_time)
print("Two stop strategy time: ", result2.total_time)

print("One stop pit stops: ", result1.pit_stops)
print("Two stop pit stops: ", result2.pit_stops)