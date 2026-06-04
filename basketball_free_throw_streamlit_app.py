
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Basketball Free Throw Stochastic Simulation", layout="wide")

st.title("🏀 Basketball Free Throw Stochastic Simulation")
st.write("""
This simulation models basketball free throws using probability and randomness.
Each free throw can be a **make** or **miss**, affected by player skill, fatigue, and pressure.
""")

# Sidebar controls
st.sidebar.header("Simulation Parameters")

base_prob = st.sidebar.slider(
    "Base free throw percentage",
    min_value=0.30,
    max_value=0.95,
    value=0.75,
    step=0.01
)

num_throws = st.sidebar.slider(
    "Number of free throws",
    min_value=10,
    max_value=500,
    value=100,
    step=10
)

fatigue_effect = st.sidebar.slider(
    "Fatigue effect per throw",
    min_value=0.000,
    max_value=0.005,
    value=0.001,
    step=0.0005
)

pressure_level = st.sidebar.slider(
    "Pressure level",
    min_value=0.00,
    max_value=0.30,
    value=0.10,
    step=0.01
)

num_simulations = st.sidebar.slider(
    "Number of repeated simulations",
    min_value=100,
    max_value=5000,
    value=1000,
    step=100
)

run_animation = st.sidebar.checkbox("Show throw-by-throw animation", value=True)

st.subheader("Model Explanation")
st.latex(r"""
P(\text{make}) = p_0 - (\text{fatigue} \times i) - \text{pressure noise}
""")
st.write("""
Where:
- \(p_0\) is the player's base free throw probability.
- \(i\) is the throw number.
- Fatigue slowly decreases the probability of making a shot.
- Pressure is modeled as random uncertainty that may reduce performance.
""")

def simulate_free_throws(base_prob, num_throws, fatigue_effect, pressure_level):
    results = []
    probabilities = []

    for i in range(num_throws):
        pressure_noise = np.random.uniform(0, pressure_level)
        current_prob = base_prob - fatigue_effect * i - pressure_noise
        current_prob = max(0.05, min(0.99, current_prob))

        shot = np.random.rand() < current_prob
        results.append(1 if shot else 0)
        probabilities.append(current_prob)

    return np.array(results), np.array(probabilities)

# Single simulation
results, probabilities = simulate_free_throws(
    base_prob, num_throws, fatigue_effect, pressure_level
)

makes = int(results.sum())
misses = num_throws - makes
percentage = makes / num_throws

col1, col2, col3 = st.columns(3)
col1.metric("Made Shots", makes)
col2.metric("Missed Shots", misses)
col3.metric("Final Free Throw %", f"{percentage * 100:.2f}%")

# Animation
if run_animation:
    st.subheader("Interactive Shot Animation")
    shot_placeholder = st.empty()
    progress = st.progress(0)

    made_count = 0
    for i, shot in enumerate(results):
        if shot == 1:
            made_count += 1
            shot_text = "✅ MADE"
        else:
            shot_text = "❌ MISSED"

        shot_placeholder.markdown(
            f"""
            ### Throw {i + 1}/{num_throws}: {shot_text}
            Current score: **{made_count} made out of {i + 1}**
            """
        )
        progress.progress((i + 1) / num_throws)
        time.sleep(0.03)

# Charts
st.subheader("Simulation Results")

df = pd.DataFrame({
    "Throw Number": np.arange(1, num_throws + 1),
    "Result": results,
    "Make Probability": probabilities,
    "Cumulative Makes": np.cumsum(results),
    "Cumulative Percentage": np.cumsum(results) / np.arange(1, num_throws + 1)
})

st.write("### Throw-by-Throw Data")
st.dataframe(df)

fig1, ax1 = plt.subplots()
ax1.plot(df["Throw Number"], df["Cumulative Percentage"])
ax1.set_xlabel("Throw Number")
ax1.set_ylabel("Cumulative Free Throw Percentage")
ax1.set_title("Cumulative Free Throw Percentage Over Time")
st.pyplot(fig1)

fig2, ax2 = plt.subplots()
ax2.plot(df["Throw Number"], df["Make Probability"])
ax2.set_xlabel("Throw Number")
ax2.set_ylabel("Probability of Making Shot")
ax2.set_title("Probability Change Due to Fatigue and Pressure")
st.pyplot(fig2)

# Repeated simulations
st.subheader("Sensitivity Analysis: Repeated Simulations")

final_scores = []


for _ in range(num_simulations):
    sim_results, _ = simulate_free_throws(
        base_prob, num_throws, fatigue_effect, pressure_level
    )
    final_scores.append(sim_results.sum())

final_scores = np.array(final_scores)

col4, col5, col6 = st.columns(3)
col4.metric("Average Made Shots", f"{final_scores.mean():.2f}")
col5.metric("Best Case", int(final_scores.max()))
col6.metric("Worst Case", int(final_scores.min()))

fig3, ax3 = plt.subplots()
ax3.hist(final_scores, bins=20)
ax3.set_xlabel("Made Shots")
ax3.set_ylabel("Frequency")
ax3.set_title("Distribution of Made Shots Across Many Simulations")
st.pyplot(fig3)

st.subheader("Insights")
st.write(f"""
Based on the simulation:
- The player made **{makes} out of {num_throws}** shots in one run.
- The average result over **{num_simulations} simulations** was **{final_scores.mean():.2f} made shots**.
- Higher fatigue and pressure generally reduce the free throw success rate.
- Because the model is stochastic, the result changes every time even with the same parameters.
""")
