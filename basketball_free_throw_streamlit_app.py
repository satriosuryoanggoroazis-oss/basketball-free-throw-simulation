import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="NBA Free Throw Simulation",
    page_icon="🏀",
    layout="wide"
)

# ==========================================================
# CUSTOM NBA STYLE CSS
# ==========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow:wght@300;400;600;700;800&display=swap');

:root {
    --nba-red: #C8102E;
    --nba-blue: #1D428A;
    --accent: #4FC3F7;
    --dark: #090E1A;
    --dark2: #101825;
    --card: #17213A;
    --muted: #91A1B8;
}

.stApp {
    background: radial-gradient(circle at top right, rgba(29,66,138,0.28), transparent 30%),
                linear-gradient(135deg, #090E1A 0%, #101825 55%, #090E1A 100%);
    color: #E8EDF5;
    font-family: 'Barlow', sans-serif;
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #101825 0%, #090E1A 100%);
    border-right: 1px solid rgba(79,195,247,0.18);
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-family: 'Bebas Neue', sans-serif;
    letter-spacing: 1px;
    color: #4FC3F7;
}

.nba-header {
    background: linear-gradient(135deg, rgba(9,14,26,0.95), rgba(16,24,37,0.95));
    border: 1px solid rgba(79,195,247,0.24);
    border-bottom: 3px solid #1D428A;
    border-radius: 18px;
    padding: 24px 30px;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 18px;
}

.logo-ball {
    font-size: 58px;
}

.title-main {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 52px;
    line-height: 0.95;
    letter-spacing: 3px;
    color: #FFFFFF;
}

.title-main span {
    color: #C8102E;
}

.subtitle {
    color: #91A1B8;
    font-size: 15px;
    letter-spacing: 1px;
    margin-top: 7px;
}

.badge {
    margin-left: auto;
    padding: 8px 15px;
    border-radius: 999px;
    border: 1px solid #C8102E;
    color: #ff6b6b;
    background: rgba(200,16,46,0.12);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
}

.section-title {
    color: #4FC3F7;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 28px;
    letter-spacing: 2px;
    margin-top: 22px;
    margin-bottom: 10px;
}

.stat-card {
    background: linear-gradient(180deg, #1A2540 0%, #141C31 100%);
    border: 1px solid rgba(79,195,247,0.23);
    border-radius: 16px;
    padding: 20px 12px;
    text-align: center;
    position: relative;
    overflow: hidden;
    min-height: 120px;
}

.stat-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: #1D428A;
}

.stat-card.red::before {
    background: #C8102E;
}

.stat-card.cyan::before {
    background: #4FC3F7;
}

.stat-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 44px;
    color: #4FC3F7;
    line-height: 1;
}

.stat-card.red .stat-value {
    color: #ff6b6b;
}

.stat-label {
    color: #91A1B8;
    font-size: 12px;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 8px;
}

.panel {
    background: linear-gradient(180deg, rgba(26,37,64,0.98), rgba(16,24,37,0.98));
    border: 1px solid rgba(79,195,247,0.20);
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 18px;
}

.court {
    height: 310px;
    border-radius: 16px;
    border: 3px solid rgba(255,255,255,0.35);
    background:
      linear-gradient(90deg, rgba(0,0,0,0.10) 1px, transparent 1px),
      linear-gradient(0deg, rgba(0,0,0,0.08) 1px, transparent 1px),
      linear-gradient(135deg, #C68642 0%, #D39A58 100%);
    background-size: 36px 36px, 36px 36px, auto;
    position: relative;
    overflow: hidden;
    display:flex;
    align-items:center;
    justify-content:center;
}

.paint {
    position:absolute;
    top: 18px;
    width: 190px;
    height: 230px;
    border: 4px solid rgba(255,255,255,0.80);
    background: rgba(200,16,46,0.16);
}

.rim {
    position:absolute;
    top: 44px;
    width: 78px;
    height: 22px;
    border: 5px solid #E87722;
    border-radius: 50%;
    box-shadow: 0 4px 0 rgba(0,0,0,0.22);
}

.backboard {
    position:absolute;
    top: 26px;
    width: 130px;
    height: 12px;
    border: 3px solid rgba(255,255,255,0.85);
    background: rgba(180,220,255,0.18);
}

.player {
    position:absolute;
    bottom: 34px;
    font-size: 86px;
    filter: drop-shadow(0 8px 8px rgba(0,0,0,0.35));
}

.shot-result {
    position:absolute;
    right: 28px;
    bottom: 28px;
    background: rgba(9,14,26,0.82);
    border: 1px solid rgba(79,195,247,0.35);
    border-radius: 14px;
    padding: 14px 18px;
    min-width: 190px;
    text-align:center;
}

.shot-big-made {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 38px;
    color: #4FC3F7;
    letter-spacing: 2px;
}

.shot-big-miss {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 38px;
    color: #ff6b6b;
    letter-spacing: 2px;
}

.small-muted {
    color: #91A1B8;
    font-size: 13px;
}

.insight-card {
    background: #111B31;
    border-left: 5px solid #1D428A;
    border-radius: 14px;
    padding: 18px;
    min-height: 140px;
}

.insight-card.red {
    border-left-color: #C8102E;
}

.insight-card.cyan {
    border-left-color: #4FC3F7;
}

.insight-title {
    color: #91A1B8;
    font-size: 12px;
    letter-spacing: 1px;
    text-transform: uppercase;
    font-weight: 700;
}

.insight-value {
    font-family: 'Bebas Neue', sans-serif;
    color: #4FC3F7;
    font-size: 38px;
    margin-top: 6px;
}

.footer {
    color: #91A1B8;
    text-align: center;
    font-size: 13px;
    padding: 22px;
    border-top: 1px solid rgba(79,195,247,0.20);
    margin-top: 25px;
}

div.stButton > button {
    background: #C8102E;
    color: white;
    border-radius: 12px;
    border: none;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 22px;
    letter-spacing: 2px;
    padding: 0.65rem 1rem;
    width: 100%;
}

div.stButton > button:hover {
    background: #E8192D;
    color: white;
    border: none;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    background-color: #17213A;
    border-radius: 999px;
    color: #91A1B8;
    padding: 8px 18px;
}

.stTabs [aria-selected="true"] {
    background-color: #1D428A;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# FUNCTIONS
# ==========================================================
def simulate_free_throws(base_probability, throws, fatigue, pressure, clutch=False):
    results = []
    probabilities = []

    for i in range(throws):
        pressure_noise = np.random.uniform(0, pressure)

        if clutch and i >= throws - 10:
            pressure_noise += np.random.uniform(0.05, 0.15)

        current_probability = base_probability - fatigue * i - pressure_noise
        current_probability = max(0.05, min(0.99, current_probability))

        made = np.random.rand() < current_probability
        results.append(1 if made else 0)
        probabilities.append(current_probability)

    return np.array(results), np.array(probabilities)


def run_monte_carlo(base_probability, throws, fatigue, pressure, simulations, clutch=False):
    scores = []
    percentages = []

    for _ in range(simulations):
        sim_results, _ = simulate_free_throws(
            base_probability,
            throws,
            fatigue,
            pressure,
            clutch
        )
        scores.append(sim_results.sum())
        percentages.append(sim_results.mean())

    return np.array(scores), np.array(percentages)


def metric_card(value, label, color_class=""):
    st.markdown(
        f"""
        <div class="stat-card {color_class}">
            <div class="stat-value">{value}</div>
            <div class="stat-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def court_panel(result_text, made_counter, total_counter, num_throws):
    result_class = "shot-big-made" if result_text == "MADE" else "shot-big-miss"
    icon = "✅" if result_text == "MADE" else "❌"

    st.markdown(
        f"""
        <div class="court">
            <div class="paint"></div>
            <div class="backboard"></div>
            <div class="rim"></div>
            <div class="player">🏀</div>
            <div class="shot-result">
                <div class="{result_class}">{icon} {result_text}</div>
                <div class="small-muted">Throw {total_counter}/{num_throws}</div>
                <div class="small-muted">Score: {made_counter} made</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# HEADER
# ==========================================================
st.markdown(
    """
    <div class="nba-header">
        <div class="logo-ball">🏀</div>
        <div>
            <div class="title-main">NBA <span>FREE THROW</span> SIMULATION</div>
            <div class="subtitle">STOCHASTIC MODELING · FATIGUE + PRESSURE + MONTE CARLO</div>
        </div>
        <div class="badge">UGM SMS PROJECT</div>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# SIDEBAR
# ==========================================================
st.sidebar.header("PARAMETER PEMAIN")

profile = st.sidebar.selectbox(
    "Player Profile",
    ["NBA Average", "Elite Shooter", "Average Guard", "Big Man", "Poor Shooter", "Custom"]
)

profile_values = {
    "NBA Average": 0.78,
    "Elite Shooter": 0.90,
    "Average Guard": 0.85,
    "Big Man": 0.65,
    "Poor Shooter": 0.55,
    "Custom": 0.75
}

base_prob = st.sidebar.slider(
    "FT Make %",
    min_value=0.30,
    max_value=0.99,
    value=float(profile_values[profile]),
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

st.sidebar.header("SCENARIO MODIFIERS")
clutch_mode = st.sidebar.checkbox("Clutch / Late Game Pressure", value=True)
show_animation = st.sidebar.checkbox("Live Free Throw Animation", value=True)

run_clicked = st.sidebar.button("RUN SIMULATION")

st.sidebar.markdown("""
---
**Model**

FTA outcome = Bernoulli trial  
Season outcome = Monte Carlo repetition  

This app focuses on pressure and fatigue effects on free throw performance.
""")

# ==========================================================
# SIMULATION
# ==========================================================
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
single_ft_percent = makes / num_throws
avg_makes = final_scores.mean()
low_ci = np.percentile(final_scores, 2.5)
high_ci = np.percentile(final_scores, 97.5)

# ==========================================================
# PLAYER TABS
# ==========================================================
st.markdown('<div class="section-title">PILIH PROFIL PEMAIN</div>', unsafe_allow_html=True)
tabs = st.tabs(["🏀 NBA Average", "⭐ Elite Shooter", "🔵 Guard", "🔴 Big Man", "❌ Poor Shooter"])

with tabs[0]:
    st.write("NBA average profile uses around **78%** base free throw accuracy.")
with tabs[1]:
    st.write("Elite shooter profile uses around **90%** base free throw accuracy.")
with tabs[2]:
    st.write("Average guard profile uses around **85%** base free throw accuracy.")
with tabs[3]:
    st.write("Big man profile uses around **65%** base free throw accuracy.")
with tabs[4]:
    st.write("Poor shooter profile uses around **55%** base free throw accuracy.")

# ==========================================================
# METRIC CARDS
# ==========================================================
st.markdown('<div class="section-title">SIMULATION RESULTS</div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    metric_card(makes, "Made Shots")
with c2:
    metric_card(misses, "Missed Shots", "red")
with c3:
    metric_card(f"{single_ft_percent*100:.1f}%", "Single Run FT%", "cyan")
with c4:
    metric_card(f"{avg_makes:.1f}", "Avg Makes")
with c5:
    metric_card(f"{int(final_scores.max())}", "Best Run", "red")

# ==========================================================
# LIVE COURT
# ==========================================================
st.markdown('<div class="section-title">LIVE FREE THROW ANIMATION</div>', unsafe_allow_html=True)

court_box = st.empty()

if show_animation:
    made_counter = 0
    progress = st.progress(0)

    for i, shot in enumerate(results):
        if shot == 1:
            made_counter += 1
            court_box.markdown(court_panel("MADE", made_counter, i + 1, num_throws), unsafe_allow_html=True)
        else:
            court_box.markdown(court_panel("MISS", made_counter, i + 1, num_throws), unsafe_allow_html=True)

        progress.progress((i + 1) / num_throws)
        time.sleep(0.015)
else:
    court_box.markdown(court_panel("MADE" if results[-1] == 1 else "MISS", makes, num_throws, num_throws), unsafe_allow_html=True)

# ==========================================================
# DATA
# ==========================================================
df = pd.DataFrame({
    "Throw Number": np.arange(1, num_throws + 1),
    "Result": ["Made" if x == 1 else "Missed" for x in results],
    "Make Probability": probabilities,
    "Cumulative Makes": np.cumsum(results),
    "Cumulative FT%": np.cumsum(results) / np.arange(1, num_throws + 1)
})

# ==========================================================
# CHARTS
# ==========================================================
st.markdown('<div class="section-title">MONTE CARLO DISTRIBUTION CHARTS</div>', unsafe_allow_html=True)

chart1, chart2 = st.columns(2)

with chart1:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    fig, ax = plt.subplots()
    ax.plot(df["Throw Number"], df["Cumulative FT%"])
    ax.set_title("Cumulative Free Throw Percentage")
    ax.set_xlabel("Throw Number")
    ax.set_ylabel("Cumulative FT%")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

with chart2:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    fig, ax = plt.subplots()
    ax.plot(df["Throw Number"], df["Make Probability"])
    ax.set_title("Make Probability Over Time")
    ax.set_xlabel("Throw Number")
    ax.set_ylabel("Probability")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

chart3, chart4 = st.columns(2)

with chart3:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    fig, ax = plt.subplots()
    ax.hist(final_scores, bins=20)
    ax.set_title("Distribution of Made Shots")
    ax.set_xlabel("Made Shots")
    ax.set_ylabel("Frequency")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

with chart4:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    pressure_values = np.linspace(0, 0.30, 10)
    avg_makes_by_pressure = []

    for p in pressure_values:
        temp_scores, _ = run_monte_carlo(
            base_prob,
            num_throws,
            fatigue_effect,
            p,
            300,
            clutch_mode
        )
        avg_makes_by_pressure.append(temp_scores.mean())

    fig, ax = plt.subplots()
    ax.plot(pressure_values, avg_makes_by_pressure, marker="o")
    ax.set_title("Sensitivity: Pressure vs Average Makes")
    ax.set_xlabel("Pressure Level")
    ax.set_ylabel("Average Made Shots")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# COMPARISON CARDS
# ==========================================================
st.markdown('<div class="section-title">PLAYER COMPARISON</div>', unsafe_allow_html=True)

p1, p2, p3, p4 = st.columns(4)

comparison_data = [
    ("Guard", "85%", int(0.85 * num_throws)),
    ("NBA Average", "78%", int(0.78 * num_throws)),
    ("Big Man", "65%", int(0.65 * num_throws)),
    ("Elite Shooter", "90%", int(0.90 * num_throws)),
]

for col, (name, pct, expected) in zip([p1, p2, p3, p4], comparison_data):
    with col:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-label">{name}</div>
                <div class="stat-value">{pct}</div>
                <div class="stat-label">Expected Makes: {expected}/{num_throws}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ==========================================================
# INSIGHTS
# ==========================================================
st.markdown('<div class="section-title">KEY INSIGHTS</div>', unsafe_allow_html=True)

i1, i2, i3 = st.columns(3)

with i1:
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">Average Makes</div>
            <div class="insight-value">{avg_makes:.1f}</div>
            <div class="small-muted">Average result across {num_simulations} Monte Carlo runs.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with i2:
    st.markdown(
        f"""
        <div class="insight-card red">
            <div class="insight-title">Worst Run</div>
            <div class="insight-value">{int(final_scores.min())}</div>
            <div class="small-muted">Lowest number of made shots caused by randomness, fatigue, and pressure.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with i3:
    st.markdown(
        f"""
        <div class="insight-card cyan">
            <div class="insight-title">95% Confidence Interval</div>
            <div class="insight-value">{low_ci:.0f}–{high_ci:.0f}</div>
            <div class="small-muted">Most expected results fall inside this interval.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================================
# TABLE
# ==========================================================
with st.expander("Show Throw-by-Throw Data"):
    st.dataframe(df, use_container_width=True)

# ==========================================================
# FOOTER
# ==========================================================
st.markdown(
    """
    <div class="footer">
        <strong>Model:</strong> Bernoulli Trial + Fatigue Function + Pressure Noise + Monte Carlo Simulation<br>
        <em>Stochastic Modeling and Simulation Project — Universitas Gadjah Mada</em>
    </div>
    """,
    unsafe_allow_html=True
)
