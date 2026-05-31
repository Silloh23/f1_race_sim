import numpy as np

class MonteCarloEngine:
    def __init__(self, simulator, n_runs=500):
        self.simulator = simulator
        self.n_runs = n_runs
        
    def evaluate_strategy(self, strategy):
        results = []
        
        for i in range(self.n_runs):
            state = self.simulator.run(strategy)
            results.append(state.total_time)
            
        return {
            "mean_time" : np.mean(results),
            "std_time" : np.std(results),
            "all_results" : results
        }