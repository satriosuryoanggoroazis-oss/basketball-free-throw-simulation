import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

st.set_page_config(
    page_title="Basketball Free Throw Simulation",
    page_icon="🏀",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #07111f 0%, #0f1c35 50%, #07111f 100%);
    color: white;
}
.block-container {
    padding-top: 1.5rem;
}
.big-title {
    font-size: 46px;
    font-weight: 900;
    color: white;
    margin-bottom: 0px;
}
.red-text {
    color: #ff4b4b;
}
.subtitle {
    color: #9fb3c8;
    font-size: 16px;
    margin-bottom: 25px;
}
.card {
    background-color: #14213d;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid rgba(79,195,247,0.25);
    text-align: center;
}
.metric-value {
    font-size: 34px;
    font-weight: 900;
    color: #4fc3f7;
}
.metric-label {
    color: #9fb3c8;
    font-size: 13px;
}
.section-title {
    font-size: 24px;
    font-weight: 800;
    color: #4fc3f7;
    margin-top: 25px;
    margin-bottom: 10px;
}
.shot-made {
    color: #4fc3f7;
    font-size: 34px;
    font-weight: 900;
}
.shot-missed {
    color: #ff4b4b;
    font-size: 34px;
    font-weight: 900;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="big-title">🏀 Basketball <span class="red-text">Free Throw</span> Simulation</div>
<div class="subtitle">
Stochastic simulation of free throw performance under fatigue, pressure, and randomness.
</div>
""", unsafe_allow_html=True)

st.sidebar.title("🏀 Simulation Controls")

player_profile = st.sidebar.selectbox(
    "Choose Player Profile",
    [
        "NBA Average",
        "Elite Shooter",
        "Average Guard",
        "Big Man",
        "Poor Free Throw Shooter",
        "Custom"
    ]
)

profiles = {
    "NBA Average": 0.78,
    "Elite Shooter": 0.90,
    "Average Guard": 0.85,
    "Big Man": 0.65,
    "Poor Free Throw Shooter": 0.55,
    "Custom": 0.75
}

default_prob = profiles[player_profile]

base_prob = st.sidebar.slider(
    "Base Free Throw Percentage",
    min_value=0.30,
    max_value=0.99,
    value=float(default_prob),
    step=0.01
)

num_throws = st.sidebar.slider(
    "Number of Free Throws",
    min_value=10,
    max_value=300,
    value=100,
    step=10
)

fatigue_effect = st.sidebar.slider(
    "Fatigue Effect per Throw",
    min_value=0.000,
    max_value=0.006,
    value=0.001,
    step=0.0005,
    format="%.4f"
)

pressure_level = st.sidebar.slider(
    "Pressure Level",
    min_value=0.00,
    max_value=0.30,
    value=0.10,
    step=0.01
)

num_simulations = st.sidebar.slider(
    "Monte Carlo Runs",
    min_value=100,
    max_value=5000,
    value=1000,
    step=100
)

clutch_mode = st.sidebar.checkbox("Clutch Mode: last 10 shots have extra pressure", value=True)
show_animation = st.sidebar.checkbox("Show Shot Animation", value=True)


def simulate_free_throws(base_probability, throws, fatigue, pressure, clutch=False):
    results = []
    probabilities = []

    for i in range(throws):
        random_pressure = np.random.uniform(0, pressure)

        if clutch and i >= throws - 10:
            random_pressure += np.random.uniform(0.05, 0.15)

        current_probability = base_probability - (fatigue * i) - random_pressure
        current_probability = max(0.05, min(0.99, current_probability))

        shot_made = np.random.rand() < current_probability

        results.append(1 if shot_made else 0)
        probabilities.append(current_probability)

    return np.array(results), np.array(probabilities)


def run_monte_carlo(base_probability, throws, fatigue, pressure, simulations, clutch=False):
    final_scores = []
    final_percentages = []

    for _ in range(simulations):
        sim_results, _ = simulate_free_throws(
            base_probability,
            throws,
            fatigue,
            pressure,
            clutch
        )
        final_scores.append(sim_results.sum())
        final_percentages.append(sim_results.mean())

    return np.array(final_scores), np.array(final_percentages)


results, probabilities = simulate_free_throws(
    base_prob,
    num_throws,
    fatigue_effect,
    pressure_level,
    clutch_mode
)

final_scores, final_percentages = run_monte_carlo(
    base_prob,
    num_throws,
    fatigue_effect,
    pressure_level,
    num_simulations,
    clutch_mode
)

makes = int(results.sum())
misses = int(num_throws - makes)
shot_percentage = makes / num_throws

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="card">
        <div class="metric-value">{makes}</div>
        <div class="metric-label">Made Shots</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
        <div class="metric-value" style="color:#ff4b4b;">{misses}</div>
        <div class="metric-label">Missed Shots</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card">
        <div class="metric-value">{shot_percentage*100:.1f}%</div>
        <div class="metric-label">Single Run FT%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="card">
        <div class="metric-value">{final_scores.mean():.1f}</div>
        <div class="metric-label">Average Makes</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-title">📌 Stochastic Model</div>', unsafe_allow_html=True)

st.write("""
Each free throw is modeled as a Bernoulli trial, where the outcome is either made or missed.
The probability of making a shot changes depending on fatigue and pressure.
""")

st.latex(r"""
P(\text{make}) = p_0 - (f \times i) - \epsilon
""")

st.write("""
Where:
- p0 = base free throw probability
- f = fatigue effect per throw
- i = throw number
- epsilon = random pressure effect
""")

st.markdown('<div class="section-title">🎬 Live Free Throw Animation</div>', unsafe_allow_html=True)

if show_animation:
    placeholder = st.empty()
    progress_bar = st.progress(0)

    made_counter = 0

    for i, shot in enumerate(results):
        if shot == 1:
            made_counter += 1
            placeholder.markdown(
                f"""
                <div class="card">
                    <div class="shot-made">✅ MADE</div>
                    <p>Throw {i+1}/{num_throws}</p>
                    <p>Score: {made_counter} made out of {i+1}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            placeholder.markdown(
                f"""
                <div class="card">
                    <div class="shot-missed">❌ MISSED</div>
                    <p>Throw {i+1}/{num_throws}</p>
                    <p>Score: {made_counter} made out of {i+1}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        progress_bar.progress((i + 1) / num_throws)
        time.sleep(0.02)
else:
    st.info("Animation is turned off. Enable it from the sidebar.")

df = pd.DataFrame({
    "Throw Number": np.arange(1, num_throws + 1),
    "Result": ["Made" if x == 1 else "Missed" for x in results],
    "Make Probability": probabilities,
    "Cumulative Makes": np.cumsum(results),
    "Cumulative FT%": np.cumsum(results) / np.arange(1, num_throws + 1)
})

st.markdown('<div class="section-title">📋 Throw-by-Throw Data</div>', unsafe_allow_html=True)
st.dataframe(df, use_container_width=True)

st.markdown('<div class="section-title">📊 Simulation Charts</div>', unsafe_allow_html=True)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    fig1, ax1 = plt.subplots()
    ax1.plot(df["Throw Number"], df["Cumulative FT%"])
    ax1.set_title("Cumulative Free Throw Percentage")
    ax1.set_xlabel("Throw Number")
    ax1.set_ylabel("Cumulative FT%")
    ax1.grid(True, alpha=0.3)
    st.pyplot(fig1)

with chart_col2:
    fig2, ax2 = plt.subplots()
    ax2.plot(df["Throw Number"], df["Make Probability"])
    ax2.set_title("Make Probability Over Time")
    ax2.set_xlabel("Throw Number")
    ax2.set_ylabel("Probability")
    ax2.grid(True, alpha=0.3)
    st.pyplot(fig2)

chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    fig3, ax3 = plt.subplots()
    ax3.hist(final_scores, bins=20)
    ax3.set_title("Monte Carlo Distribution of Made Shots")
    ax3.set_xlabel("Made Shots")
    ax3.set_ylabel("Frequency")
    ax3.grid(True, alpha=0.3)
    st.pyplot(fig3)

with chart_col4:
    pressure_values = np.linspace(0, 0.30, 10)
    avg_makes_by_pressure = []

    for p in pressure_values:
        scores, _ = run_monte_carlo(
            base_prob,
            num_throws,
            fatigue_effect,
            p,
            300,
            clutch_mode
        )
        avg_makes_by_pressure.append(scores.mean())

    fig4, ax4 = plt.subplots()
    ax4.plot(pressure_values, avg_makes_by_pressure, marker="o")
    ax4.set_title("Sensitivity Analysis: Pressure vs Average Makes")
    ax4.set_xlabel("Pressure Level")
    ax4.set_ylabel("Average Made Shots")
    ax4.grid(True, alpha=0.3)
    st.pyplot(fig4)

st.markdown('<div class="section-title">💡 Key Insights</div>', unsafe_allow_html=True)

low_ci = np.percentile(final_scores, 2.5)
high_ci = np.percentile(final_scores, 97.5)

st.write(f"""
Based on {num_simulations} Monte Carlo simulations:

- The average number of made shots is {final_scores.mean():.2f} out of {num_throws}.
- The best simulation produced {final_scores.max()} made shots.
- The worst simulation produced {final_scores.min()} made shots.
- The 95% confidence interval is approximately {low_ci:.0f} to {high_ci:.0f} made shots.
- Increasing pressure generally decreases the average number of made shots.
- Fatigue causes the probability of success to decrease over time.
""")

st.markdown("---")
st.caption("Stochastic Modeling and Simulation Project — Basketball Free Throw Performance")
