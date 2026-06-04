import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="NBA Free Throw Simulation",
    page_icon="🏀",
    layout="wide"
)

# =========================
# DARK NBA CSS
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow+Condensed:wght@400;600;700&family=Barlow:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Barlow', sans-serif;
}

.stApp {
    background: #090E1A;
    color: #E8EDF5;
}

.block-container {
    padding-top: 1.2rem;
    padding-left: 2.2rem;
    padding-right: 2.2rem;
}

[data-testid="stSidebar"] {
    background: #101825;
    border-right: 1px solid rgba(29,66,138,0.35);
}

[data-testid="stSidebar"] label {
    color: #A7B5C9 !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #4FC3F7;
    font-family: 'Barlow Condensed', sans-serif;
    letter-spacing: 2px;
}

.nba-header {
    background: linear-gradient(135deg, #090E1A 0%, #0D1830 60%, #090E1A 100%);
    border-bottom: 2px solid #1D428A;
    border-radius: 0 0 18px 18px;
    padding: 24px 30px;
    margin-bottom: 22px;
    display: flex;
    align-items: center;
    gap: 18px;
}

.ball-logo {
    width: 72px;
    height: 72px;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 25%, #F28C28, #C8102E);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 44px;
    border: 2px solid #1D428A;
}

.header-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 54px;
    letter-spacing: 4px;
    color: white;
    line-height: 0.9;
}

.header-title span {
    color: #C8102E;
}

.header-subtitle {
    font-family: 'Barlow Condensed', sans-serif;
    color: #7A8A9E;
    font-size: 16px;
    letter-spacing: 1.4px;
    margin-top: 8px;
}

.header-badge {
    margin-left: auto;
    color: #C8102E;
    border: 1px solid #C8102E;
    background: rgba(200,16,46,0.15);
    padding: 8px 14px;
    border-radius: 99px;
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 13px;
    letter-spacing: 1.5px;
}

.section-title {
    font-family: 'Barlow Condensed', sans-serif;
    color: #1D428A;
    font-weight: 700;
    letter-spacing: 4px;
    text-transform: uppercase;
    font-size: 18px;
    margin-top: 28px;
    margin-bottom: 14px;
    border-bottom: 1px solid rgba(29,66,138,0.35);
    padding-bottom: 8px;
}

.stat-card {
    background: #1A2540;
    border: 1px solid rgba(29,66,138,0.35);
    border-radius: 14px;
    padding: 18px 14px;
    text-align: center;
    min-height: 120px;
    position: relative;
    overflow: hidden;
}

.stat-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
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
    color: #4FC3F7;
    font-size: 46px;
    line-height: 1;
}

.stat-card.red .stat-value {
    color: #FF6B6B;
}

.stat-label {
    color: #7A8A9E;
    font-size: 12px;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-top: 8px;
}

.chart-card {
    background: #1A2540;
    border: 1px solid rgba(29,66,138,0.35);
    border-radius: 18px;
    padding: 22px 24px 10px 24px;
    margin-bottom: 18px;
}

.chart-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 3px;
    color: #A7B5C9;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.court-card {
    background: #1A2540;
    border: 1px solid rgba(29,66,138,0.35);
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 18px;
}

.court {
    height: 280px;
    border-radius: 12px;
    border: 2px solid rgba(255,255,255,0.65);
    background:
        linear-gradient(90deg, rgba(0,0,0,0.08) 1px, transparent 1px),
        linear-gradient(0deg, rgba(0,0,0,0.08) 1px, transparent 1px),
        linear-gradient(135deg, #C68642, #D6A05E);
    background-size: 34px 34px, 34px 34px, auto;
    position: relative;
    overflow: hidden;
}

.paint {
    position: absolute;
    width: 190px;
    height: 220px;
    left: 50%;
    transform: translateX(-50%);
    top: 20px;
    border: 4px solid rgba(255,255,255,0.9);
    background: rgba(200,16,46,0.18);
}

.backboard {
    position: absolute;
    top: 25px;
    left: 50%;
    transform: translateX(-50%);
    width: 140px;
    height: 12px;
    border: 3px solid rgba(255,255,255,0.95);
    background: rgba(180,220,255,0.22);
}

.rim {
    position: absolute;
    top: 49px;
    left: 50%;
    transform: translateX(-50%);
    width: 80px;
    height: 24px;
    border-radius: 50%;
    border: 5px solid #E87722;
    box-shadow: 0 4px 0 rgba(0,0,0,0.35);
}

.player {
    position: absolute;
    bottom: 32px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 76px;
}

.result-box {
    position: absolute;
    right: 26px;
    bottom: 24px;
    min-width: 190px;
    padding: 14px 16px;
    background: rgba(9,14,26,0.86);
    border: 1px solid rgba(79,195,247,0.35);
    border-radius: 14px;
    text-align: center;
}

.result-made {
    font-family: 'Bebas Neue', sans-serif;
    color: #4FC3F7;
    font-size: 38px;
    letter-spacing: 2px;
}

.result-miss {
    font-family: 'Bebas Neue', sans-serif;
    color: #FF6B6B;
    font-size: 38px;
    letter-spacing: 2px;
}

.muted {
    color: #7A8A9E;
    font-size: 13px;
}

.insight-card {
    background: #1A2540;
    border: 1px solid rgba(29,66,138,0.35);
    border-left: 4px solid #1D428A;
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
    font-family: 'Barlow Condensed', sans-serif;
    color: #A7B5C9;
    font-size: 15px;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.insight-value {
    font-family: 'Bebas Neue', sans-serif;
    color: #4FC3F7;
    font-size: 42px;
    margin-top: 5px;
}

div.stButton > button {
    background: #C8102E;
    color: white;
    border: none;
    border-radius: 9px;
    width: 100%;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 24px;
    letter-spacing: 3px;
}

div.stButton > button:hover {
    background: #E8192D;
    color: white;
}

.footer {
    color: #7A8A9E;
    text-align: center;
    padding: 20px;
    border-top: 1px solid rgba(29,66,138,0.35);
    margin-top: 25px;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# FUNCTIONS
# =========================
def simulate_free_throws(base_probability, throws, fatigue, pressure, clutch=False):
    results = []
    probabilities = []

    for i in range(throws):
        pressure_noise = np.random.uniform(0, pressure)

        if clutch and i >= throws - 10:
            pressure_noise += np.random.uniform(0.05, 0.15)

        prob = base_probability - fatigue * i - pressure_noise
        prob = max(0.05, min(0.99, prob))

        made = np.random.rand() < prob
        results.append(1 if made else 0)
        probabilities.append(prob)

    return np.array(results), np.array(probabilities)


def run_monte_carlo(base_probability, throws, fatigue, pressure, simulations, clutch=False):
    scores = []

    for _ in range(simulations):
        sim_results, _ = simulate_free_throws(
            base_probability,
            throws,
            fatigue,
            pressure,
            clutch
        )
        scores.append(sim_results.sum())

    return np.array(scores)


def metric_card(value, label, kind=""):
    st.markdown(
        f"""
        <div class="stat-card {kind}">
            <div class="stat-value">{value}</div>
            <div class="stat-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def draw_chart_card(title):
    st.markdown(f'<div class="chart-card"><div class="chart-title">{title}</div>', unsafe_allow_html=True)


def close_chart_card():
    st.markdown('</div>', unsafe_allow_html=True)


def style_matplotlib(fig, ax):
    fig.patch.set_facecolor("#1A2540")
    ax.set_facecolor("#1A2540")

    ax.tick_params(colors="#7A8A9E", labelsize=9)
    ax.xaxis.label.set_color("#A7B5C9")
    ax.yaxis.label.set_color("#A7B5C9")
    ax.title.set_color("#A7B5C9")

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.grid(True, color="#263452", alpha=0.55, linewidth=0.8)
    return fig, ax


def court_html(result, made_counter, current_throw, total_throw):
    result_class = "result-made" if result == "MADE" else "result-miss"
    icon = "✅" if result == "MADE" else "❌"

    return f"""
    <div class="court">
        <div class="paint"></div>
        <div class="backboard"></div>
        <div class="rim"></div>
        <div class="player">🏀</div>
        <div class="result-box">
            <div class="{result_class}">{icon} {result}</div>
            <div class="muted">Throw {current_throw}/{total_throw}</div>
            <div class="muted">Score: {made_counter} made</div>
        </div>
    </div>
    """


# =========================
# HEADER
# =========================
st.markdown("""
<div class="nba-header">
    <div class="ball-logo">🏀</div>
    <div>
        <div class="header-title">NBA <span>FREE THROW</span> SIMULATION</div>
        <div class="header-subtitle">STOCHASTIC MODELING · FATIGUE + PRESSURE + MONTE CARLO</div>
    </div>
    <div class="header-badge">UGM SMS PROJECT</div>
</div>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
st.sidebar.header("PARAMETER PEMAIN")

profile = st.sidebar.selectbox(
    "Quick Presets",
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
show_animation = st.sidebar.checkbox("Live Animation", value=True)

st.sidebar.button("▶ RUN SIMULATION")

st.sidebar.markdown("""
---
**Model**

Each free throw is a Bernoulli trial.

`P(make) = base probability - fatigue - pressure`

Monte Carlo repeats the simulation many times to observe the distribution of possible results.
""")

# =========================
# RUN SIMULATION
# =========================
results, probabilities = simulate_free_throws(
    base_prob,
    num_throws,
    fatigue_effect,
    pressure_level,
    clutch_mode
)

final_scores = run_monte_carlo(
    base_prob,
    num_throws,
    fatigue_effect,
    pressure_level,
    num_simulations,
    clutch_mode
)

makes = int(results.sum())
misses = num_throws - makes
single_percent = makes / num_throws
avg_makes = final_scores.mean()
low_ci = np.percentile(final_scores, 2.5)
high_ci = np.percentile(final_scores, 97.5)

df = pd.DataFrame({
    "Throw Number": np.arange(1, num_throws + 1),
    "Result": results,
    "Make Probability": probabilities,
    "Cumulative Makes": np.cumsum(results),
    "Cumulative FT%": np.cumsum(results) / np.arange(1, num_throws + 1)
})

# =========================
# PLAYER PROFILE INFO
# =========================
st.markdown('<div class="section-title">PILIH PROFIL PEMAIN</div>', unsafe_allow_html=True)

p1, p2, p3, p4, p5 = st.columns(5)
profile_cards = [
    ("NBA Average", "78%"),
    ("Elite Shooter", "90%"),
    ("Guard", "85%"),
    ("Big Man", "65%"),
    ("Poor Shooter", "55%")
]
for col, (name, pct) in zip([p1, p2, p3, p4, p5], profile_cards):
    with col:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-value">{pct}</div>
                <div class="stat-label">{name}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================
# RESULT CARDS
# =========================
st.markdown('<div class="section-title">SIMULATION RESULTS</div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    metric_card(makes, "Made Shots")
with c2:
    metric_card(misses, "Missed Shots", "red")
with c3:
    metric_card(f"{single_percent*100:.1f}%", "Single Run FT%", "cyan")
with c4:
    metric_card(f"{avg_makes:.1f}", "Avg Makes")
with c5:
    metric_card(int(final_scores.max()), "Best Run", "red")

# =========================
# LIVE COURT
# =========================
st.markdown('<div class="section-title">LIVE FREE THROW ANIMATION</div>', unsafe_allow_html=True)
st.markdown('<div class="court-card">', unsafe_allow_html=True)
court_placeholder = st.empty()

if show_animation:
    made_counter = 0
    progress = st.progress(0)

    for i, shot in enumerate(results):
        if shot == 1:
            made_counter += 1
            court_placeholder.markdown(court_html("MADE", made_counter, i + 1, num_throws), unsafe_allow_html=True)
        else:
            court_placeholder.markdown(court_html("MISS", made_counter, i + 1, num_throws), unsafe_allow_html=True)

        progress.progress((i + 1) / num_throws)
        time.sleep(0.012)
else:
    court_placeholder.markdown(court_html("MADE" if results[-1] == 1 else "MISS", makes, num_throws, num_throws), unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# CHARTS LIKE FRIEND'S UI
# =========================
st.markdown('<div class="section-title">MONTE CARLO DISTRIBUTION CHARTS</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    draw_chart_card("Cumulative Free Throw Percentage")
    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    ax.plot(df["Throw Number"], df["Cumulative FT%"] * 100, color="#1D428A", linewidth=3)
    ax.axhline(base_prob * 100, color="#C8102E", linestyle="--", linewidth=2)
    ax.set_xlabel("Throw Number")
    ax.set_ylabel("FT%")
    ax.set_ylim(0, 100)
    style_matplotlib(fig, ax)
    st.pyplot(fig, use_container_width=True)
    close_chart_card()

with col_b:
    draw_chart_card("Make Probability Over Time")
    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    ax.bar(df["Throw Number"], df["Make Probability"] * 100, color="#4FC3F7", alpha=0.85)
    ax.set_xlabel("Throw Number")
    ax.set_ylabel("Probability (%)")
    ax.set_ylim(0, 100)
    style_matplotlib(fig, ax)
    st.pyplot(fig, use_container_width=True)
    close_chart_card()

col_c, col_d = st.columns(2)

with col_c:
    draw_chart_card("Monte Carlo Distribution of Made Shots")
    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    ax.hist(final_scores, bins=22, color="#1D428A", edgecolor="#1A2540")
    ax.axvline(avg_makes, color="#C8102E", linewidth=3)
    ax.set_xlabel("Made Shots")
    ax.set_ylabel("Frequency")
    style_matplotlib(fig, ax)
    st.pyplot(fig, use_container_width=True)
    close_chart_card()

with col_d:
    draw_chart_card("Sensitivity: Pressure vs Average Makes")
    pressure_values = np.linspace(0, 0.30, 12)
    avg_by_pressure = []

    for p in pressure_values:
        temp_scores = run_monte_carlo(
            base_prob,
            num_throws,
            fatigue_effect,
            p,
            300,
            clutch_mode
        )
        avg_by_pressure.append(temp_scores.mean())

    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    ax.plot(
        pressure_values,
        avg_by_pressure,
        color="#C8102E",
        linewidth=3,
        marker="o",
        markersize=6,
        markerfacecolor="#4FC3F7",
        markeredgecolor="#C8102E",
        markeredgewidth=2
    )
    ax.fill_between(pressure_values, avg_by_pressure, color="#C8102E", alpha=0.12)
    ax.set_xlabel("Pressure Level")
    ax.set_ylabel("Average Makes")
    style_matplotlib(fig, ax)
    st.pyplot(fig, use_container_width=True)
    close_chart_card()

# =========================
# INSIGHTS
# =========================
st.markdown('<div class="section-title">KEY INSIGHTS</div>', unsafe_allow_html=True)

i1, i2, i3 = st.columns(3)

with i1:
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">Average Makes</div>
            <div class="insight-value">{avg_makes:.1f}</div>
            <div class="muted">Average result from {num_simulations} Monte Carlo simulations.</div>
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
            <div class="muted">Lowest possible result caused by pressure, fatigue, and randomness.</div>
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
            <div class="muted">Most results are expected to fall inside this interval.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# DATA TABLE
# =========================
with st.expander("Show Throw-by-Throw Data"):
    st.dataframe(df, use_container_width=True)

# =========================
# FOOTER
# =========================
st.markdown(
    """
    <div class="footer">
        <strong>Model:</strong> Bernoulli Trial + Fatigue Effect + Pressure Noise + Monte Carlo Simulation<br>
        <em>Stochastic Modeling and Simulation Project — Universitas Gadjah Mada</em>
    </div>
    """,
    unsafe_allow_html=True
)
