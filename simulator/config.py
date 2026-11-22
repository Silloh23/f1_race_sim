class RaceConfig:
    def __init__(self):
        self.total_laps = 60
        self.base_lap_time = 90

        self.degradation_rate = 0.0313  # seconds per tyre lap, FastF1 2023 fit
        self.noise_std = 0.4
        self.pit_loss = 10
