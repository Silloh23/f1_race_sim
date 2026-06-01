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
            
        mean = np.mean(results)
        std = np.std(results)
        se = std / np.sqrt(len(results))
        
        ci_low = mean - 1.96 * se
        ci_high = mean + 1.96 * se
        average = (ci_high + ci_low) / 2
        width = ci_high - ci_low
            
        return {
            "mean_time" : mean,
            "std_time" : std,
            "all_results" : results,
            "average" : average,
            "uncertainty" : width
        }