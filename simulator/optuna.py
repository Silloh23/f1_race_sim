from simulator.monte_carlo import MonteCarloEngine
from simulator.config import RaceConfig
from simulator.race import RaceSimulator

def objective1(trial):
    pit_1 = trial.suggest_int("pit_1", 10, 40)
    
    strategy = [pit_1]
    
    config = RaceConfig()
    sim = RaceSimulator(config)
    mc = MonteCarloEngine(simulator=sim, n_runs=500)
    
    result = mc.evaluate_strategy(strategy)
    
    return result["mean_time"]

def objective(trial):
    pit_1 = trial.suggest_int("pit_1", 10, 40)
    pit_2 = trial.suggest_int("pit_2", 10, 45)
    
    strategy = sorted([pit_1, pit_2])
    
    config = RaceConfig()
    sim = RaceSimulator(config)
    mc = MonteCarloEngine(simulator=sim, n_runs=500)
    
    result = mc.evaluate_strategy(strategy)
    
    return result["mean_time"]