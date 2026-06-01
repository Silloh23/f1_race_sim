# F1 Race Strategy AI Simulator

A modular simulation and optimisation framework for evaluating Formula 1 race strategies under uncertainty using Monte Carlo methods, statistical confidence intervals, and machine learning-based lap time prediction.

---

## Project Overview

This project simulates full race weekends to answer a core question:

> What is the optimal pit-stop strategy under stochastic race conditions?

It models:

* Lap time evolution
* Tire degradation
* Pit stop time loss
* Random race noise (simulating real-world variability)

and uses:

* Monte Carlo simulation
* Confidence intervals
* Bayesian/black-box optimisation (Optuna)

---

## Key Features

### Race Simulation Engine

* Physics-inspired lap time model
* Tire degradation over time
* Pit-stop reset mechanics
* Stochastic noise for realism

### Monte Carlo Evaluation

* 500 race simulations per strategy
* Distribution of finishing times
* Mean, variance, and risk analysis

### Uncertainty Quantification

* 95% confidence intervals for all strategies
* Statistical comparison of strategy performance
* Overlap analysis for decision robustness

### Strategy Optimisation (Optuna)

* Automated pit-stop strategy search
* Black-box optimisation over discrete pit windows
* Efficient exploration of strategy space

---

## Example Output

### Strategy Comparison

| Strategy | Mean Time | Uncertainty |
| -------- | --------- | ----------- |
| 1-stop   | 5538.66s  |   0.5297    |
| 2-stop   | 5538.92s  |   0.5107    |

Demonstrates statistically close performance under uncertainty.

---

## Technologies Used

* Python 3.10+
* NumPy
* Matplotlib
* Optuna (Bayesian optimisation)

---

## Project Structure

```
f1_race_sim/
│
├── main.py                  # Entry point / experiments
├── simulator/              # Core race simulation engine
│   ├── race.py
│   ├── monte_carlo.py
│   ├── strategy.py
|   ├── state.py
│   └── optuna.py
│
├── utils/
│   └── stats.py            # CI, metrics, helpers
│
└── requirements.txt
```

---

## Methodology

1. Define race environment (laps, tire degradation, pit loss)
2. Simulate full race under a given strategy
3. Run Monte Carlo simulations to capture randomness
4. Compute statistical performance metrics
5. Optimise strategy using Optuna

---

## Key Insight

Rather than relying on deterministic race outcomes, this system models **distributional performance**, enabling:

> Robust strategy optimisation under uncertainty instead of single-run optimisation.

---

## How to Run

```bash
# install dependencies
pip install -r requirements.txt

# run simulation
python main.py
```

---

## Future Improvements

* Reinforcement learning pit-stop agent
* Weather and safety car modelling
* Multi-car race interactions
* Real F1 telemetry dataset integration
* Streamlit dashboard for interactive strategy analysis

---

## What This Project Demonstrates

* Monte Carlo simulation design
* Stochastic optimisation (Optuna)
* Statistical inference (confidence intervals)
* Modular system architecture
* Experimental ML system design

---

## Author

Built as a simulation + ML systems project exploring:

> decision-making under uncertainty in dynamic racing environments

