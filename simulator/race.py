import random
import numpy as np
from .state import RaceState

class RaceSimulator:
    def __init__(self, config):
        self.config = config
        
    def simulate_lap(self, state: RaceState):
        degradation = state.tire_age * self.config.degradation_rate
        noise = np.random.normal(0, self.config.noise_std)
        
        fresh_tire_bonus = max(0, 0.5 - 0.05 * state.tire_age)
        
        lap_time = self.config.base_lap_time + degradation + noise - fresh_tire_bonus
        
        if state.just_pitted:
            lap_time += self.config.pit_loss
            state.just_pitted = False
        
        state.total_time += lap_time
        state.lap_times.append(lap_time)
        
        state.tire_age += 1
        state.lap +=1
        
    def pit_stop(self, state: RaceState):
        state.total_time += self.config.pit_loss
        state.just_pitted = True
        state.tire_age = 0
        state.pit_stops.append(state.lap)
        
    def run (self, strategy):
        state = RaceState()
        
        for lap in range (self.config.total_laps):
            if lap in strategy:
                self.pit_stop(state)
                state.tire_age = 0
            self.simulate_lap(state)
        return state