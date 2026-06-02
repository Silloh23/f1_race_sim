from simulator.config import RaceConfig
from simulator.race import RaceSimulator
from simulator.monte_carlo import MonteCarloEngine
import streamlit as st
import matplotlib.pyplot as plt
from simulator.optuna import objective, objective1
import optuna


st.set_page_config(
    page_title="F1 Race Strategy Simulator",
    layout="wide"
)

st.title("F1 Race Simulator")

st.write(
    "Monte Carlo optimisation of pit-stop strategies under uncertainty."
)

st.sidebar.header("Race Configuration")

laps = st.sidebar.slider("Race Laps", 30, 80, 50)
mc_runs = st.sidebar.slider("Monte Carlo Runs", 100, 5000, 1000)
pit_loss = st.sidebar.slider("Pit Stop Loss (seconds)", 15.0, 30.0, 22.0)

run_button = st.sidebar.button("Run Monte Carlo Simulation")
optimize_button = st.sidebar.button("Optimize Simulation")


# ------Run Monte Carlo------
if run_button:
    config = RaceConfig()
    simulator = RaceSimulator(config)
    mc = MonteCarloEngine(simulator, n_runs=mc_runs)

    one_stop = [25]
    two_stop = [15, 36]

    base_1 = simulator.run(one_stop)
    base_2 = simulator.run(two_stop)
    monte_carlo_strat1 = mc.evaluate_strategy(one_stop)
    monte_carlo_strat2 = mc.evaluate_strategy(two_stop)

    # Store in session state so results persist across reruns
    st.session_state["base_1"] = base_1
    st.session_state["base_2"] = base_2
    st.session_state["mc_strat1"] = monte_carlo_strat1
    st.session_state["mc_strat2"] = monte_carlo_strat2
    st.session_state["last_action"] = "run"

# ------Optimize------
if optimize_button:
    config = RaceConfig()
    simulator = RaceSimulator(config)
    mc = MonteCarloEngine(simulator, n_runs=mc_runs)

    study1 = optuna.create_study(direction="minimize")
    study1.optimize(objective1, n_trials=100)

    study2 = optuna.create_study(direction="minimize")
    study2.optimize(objective, n_trials=100)

    optimize_monte_carlo1 = mc.evaluate_strategy(study1.best_params)
    optimize_monte_carlo2 = mc.evaluate_strategy(study2.best_params)

    # Store in session state
    st.session_state["opt_strat1"] = optimize_monte_carlo1
    st.session_state["opt_strat2"] = optimize_monte_carlo2
    st.session_state["best_params1"] = study1.best_params
    st.session_state["best_params2"] = study2.best_params
    st.session_state["last_action"] = "optimize"


# ------Display Monte Carlo Results------
if st.session_state.get("last_action") == "run":
    base_1 = st.session_state["base_1"]
    base_2 = st.session_state["base_2"]
    mc_strat1 = st.session_state["mc_strat1"]
    mc_strat2 = st.session_state["mc_strat2"]
    
### ----- Base Strategy Plot -----
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Basic One Stop Strategy")
        metric1, metric2 = st.columns(2)
        with metric1:
            st.metric("Mean Time", f"{base_1.total_time:.2f}")
        with metric2:
            st.metric("Pit Stop Laps:", str(base_1.pit_stops))

    with col_right:
        st.subheader("Basic Two Stop Strategy")
        metric3, metric4 = st.columns(2)
        with metric3:
            st.metric("Mean Time", f"{base_2.total_time:.2f}")
        with metric4:
            st.metric("Pit Stop Laps:", str(base_2.pit_stops))


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
    st.pyplot(fig)

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Monte Carlo One Stop Strategy")
        metric1, metric2 = st.columns(2)
        with metric1:
            st.metric("Mean Time", f"{mc_strat1['mean_time']:.2f}")
        with metric2:
            st.metric("Uncertainty", f"{mc_strat1['uncertainty']:.2f}")

    with col_right:
        st.subheader("Monte Carlo Two Stop Strategy")
        metric3, metric4 = st.columns(2)
        with metric3:
            st.metric("Mean Time", f"{mc_strat2['mean_time']:.2f}")
        with metric4:
            st.metric("Uncertainty", f"{mc_strat2['uncertainty']:.2f}")

    times_1 = mc_strat1["all_results"]
    times_2 = mc_strat2["all_results"]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].hist(times_1, bins=30, alpha=0.6, label="One Stop")
    axes[0].hist(times_2, bins=30, alpha=0.6, label="Two Stop")
    axes[0].set_title("Monte Carlo Race Time Distribution")
    axes[0].set_xlabel("Race Time (s)")
    axes[0].set_ylabel("Frequency")
    axes[0].legend()
    axes[0].grid(True)

    axes[1].boxplot([times_1, times_2], tick_labels=["One Stop", "Two Stop"])
    axes[1].set_title("Monte Carlo Strategy Box Plot")
    axes[1].set_ylabel("Race Time (s)")
    axes[1].grid(True)

    plt.tight_layout()
    st.pyplot(fig)


# ------Display Optimised Results------
elif st.session_state.get("last_action") == "optimize":
    opt_strat1 = st.session_state["opt_strat1"]
    opt_strat2 = st.session_state["opt_strat2"]
    best_params1 = st.session_state["best_params1"]
    best_params2 = st.session_state["best_params2"]
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("One Stop Strategy")
        metric1, metric2 = st.columns(2)
        with metric1:
            st.metric("Mean Time", f"{opt_strat1['mean_time']:.2f}")
        with metric2:
            st.metric("Uncertainty", f"{opt_strat1['uncertainty']:.2f}")

    with col_right:
        st.subheader("Two Stop Strategy")
        metric3, metric4 = st.columns(2)
        with metric3:
            st.metric("Mean Time", f"{opt_strat2['mean_time']:.2f}")
        with metric4:
            st.metric("Uncertainty", f"{opt_strat2['uncertainty']:.2f}")

    st.subheader("Best Strategy Found")
    st.success(
        f"Optimal One Stop Strat: {best_params1}\n"
        f"Optimal Two Stop Strat: {best_params2}"
    )

    omc_1 = opt_strat1["all_results"]
    omc_2 = opt_strat2["all_results"]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].hist(omc_1, bins=30, alpha=0.6, label="One Stop")
    axes[0].hist(omc_2, bins=30, alpha=0.6, label="Two Stop")
    axes[0].set_title("Optimal Monte Carlo Race Time Distribution")
    axes[0].set_xlabel("Race Time (s)")
    axes[0].set_ylabel("Frequency")
    axes[0].legend()
    axes[0].grid(True)

    axes[1].boxplot([omc_1, omc_2], tick_labels=["One Stop", "Two Stop"])
    axes[1].set_title("Optimal Monte Carlo Strategy Box Plot")
    axes[1].set_ylabel("Race Time (s)")
    axes[1].grid(True)

    plt.tight_layout()
    st.pyplot(fig)