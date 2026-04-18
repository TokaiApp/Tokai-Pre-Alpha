import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import time
import random
from datetime import datetime, timedelta

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TOKAI — Neuro Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS (Cyber-Medical Dark Theme) ────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #070d1a 0%, #0a1628 50%, #06111f 100%);
}

/* Header */
.tokai-header {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 12px 0 20px 0;
    border-bottom: 1px solid rgba(0, 245, 212, 0.2);
    margin-bottom: 24px;
}
.tokai-logo {
    font-family: 'Share Tech Mono', monospace;
    font-size: 2.8rem;
    font-weight: 700;
    color: #00f5d4;
    letter-spacing: 8px;
    text-shadow: 0 0 20px rgba(0, 245, 212, 0.6), 0 0 40px rgba(0, 245, 212, 0.2);
    margin: 0;
}
.tokai-subtitle {
    font-size: 0.85rem;
    color: #5a8fa8;
    letter-spacing: 3px;
    text-transform: uppercase;
    font-family: 'Share Tech Mono', monospace;
}

/* Metric Cards */
.metric-card {
    background: linear-gradient(135deg, #0d1b2e, #0f2035);
    border: 1px solid rgba(0, 245, 212, 0.15);
    border-radius: 10px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, #00f5d4, #0066ff);
}
.metric-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    color: #5a8fa8;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.metric-value {
    font-family: 'Share Tech Mono', monospace;
    font-size: 2.2rem;
    font-weight: 700;
    color: #00f5d4;
    line-height: 1;
    text-shadow: 0 0 12px rgba(0, 245, 212, 0.4);
}
.metric-unit {
    font-size: 0.9rem;
    color: #5a8fa8;
    margin-left: 4px;
}

/* Section Headers */
.section-header {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #00f5d4;
    border-left: 3px solid #00f5d4;
    padding-left: 10px;
    margin: 20px 0 14px 0;
}

/* Status badges */
.badge-optimal { 
    background: rgba(0, 245, 212, 0.1); 
    border: 1px solid #00f5d4; 
    color: #00f5d4; 
    padding: 3px 10px; 
    border-radius: 4px; 
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
}
.badge-moderate { 
    background: rgba(255, 196, 0, 0.1); 
    border: 1px solid #ffc400; 
    color: #ffc400; 
    padding: 3px 10px; 
    border-radius: 4px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
}
.badge-low { 
    background: rgba(255, 60, 90, 0.1); 
    border: 1px solid #ff3c5a; 
    color: #ff3c5a; 
    padding: 3px 10px; 
    border-radius: 4px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
}

/* LUNA Panel */
.luna-panel {
    background: linear-gradient(135deg, #0a1225, #0d1b2e);
    border: 1px solid rgba(0, 102, 255, 0.3);
    border-radius: 10px;
    padding: 20px;
    position: relative;
    overflow: hidden;
}
.luna-panel::after {
    content: '';
    position: absolute;
    top: -50%; right: -20%;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(0,102,255,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.luna-id {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    color: #0066ff;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.luna-text {
    font-size: 1rem;
    color: #b8d4e8;
    line-height: 1.7;
    font-style: italic;
}

/* Focus Window Rows */
.focus-window {
    background: #0d1b2e;
    border: 1px solid rgba(0, 245, 212, 0.1);
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

/* Todo Items */
.todo-item {
    background: #0d1b2e;
    border-left: 3px solid rgba(0, 245, 212, 0.3);
    border-radius: 0 8px 8px 0;
    padding: 10px 14px;
    margin-bottom: 8px;
    font-family: 'Rajdhani', sans-serif;
    font-size: 1rem;
    color: #c8d8e8;
    display: flex;
    align-items: center;
    gap: 10px;
}
.todo-done {
    border-left-color: #00f5d4;
    color: #5a8fa8;
    text-decoration: line-through;
}

/* Streamlit element overrides */
div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060c18 0%, #08111f 100%);
    border-right: 1px solid rgba(0, 245, 212, 0.1);
}
.stButton > button {
    background: linear-gradient(135deg, rgba(0,245,212,0.1), rgba(0,102,255,0.1));
    border: 1px solid rgba(0, 245, 212, 0.4);
    color: #00f5d4;
    font-family: 'Share Tech Mono', monospace;
    letter-spacing: 2px;
    font-size: 0.8rem;
    border-radius: 6px;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    background: rgba(0, 245, 212, 0.2);
    border-color: #00f5d4;
    box-shadow: 0 0 12px rgba(0, 245, 212, 0.2);
}
.stTextInput > div > div > input {
    background: #0d1b2e;
    border: 1px solid rgba(0, 245, 212, 0.2);
    color: #c8d8e8;
    border-radius: 6px;
    font-family: 'Rajdhani', sans-serif;
}
.stTextInput > div > div > input:focus {
    border-color: #00f5d4;
    box-shadow: 0 0 8px rgba(0, 245, 212, 0.15);
}
hr {
    border-color: rgba(0, 245, 212, 0.1) !important;
}
</style>
""", unsafe_allow_html=True)


# ─── Session State Init ───────────────────────────────────────────────────────
if "focus_history" not in st.session_state:
    st.session_state.focus_history = []
if "timestamp_history" not in st.session_state:
    st.session_state.timestamp_history = []
if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {"text": "Review morning notes", "done": False},
        {"text": "Deep work block: project spec", "done": False},
        {"text": "Reply to priority emails", "done": False},
    ]
if "task_done_set" not in st.session_state:
    st.session_state.task_done_set = set()
if "auto_refresh" not in st.session_state:
    st.session_state.auto_refresh = True
if "refresh_count" not in st.session_state:
    st.session_state.refresh_count = 0
if "bio_energy" not in st.session_state:
    st.session_state.bio_energy = random.uniform(60, 90)
if "noise_level" not in st.session_state:
    st.session_state.noise_level = random.uniform(10, 40)


# ─── EEG Simulation ──────────────────────────────────────────────────────────
def generate_eeg_signal(n=256, fs=256):
    t = np.linspace(0, 1, n)
    alpha_freq = random.uniform(8, 13)
    beta_freq = random.uniform(13, 30)
    alpha_amp = random.uniform(0.5, 2.0)
    beta_amp = random.uniform(0.2, 1.5)
    noise = np.random.normal(0, 0.3, n)
    alpha = alpha_amp * np.sin(2 * np.pi * alpha_freq * t)
    beta = beta_amp * np.sin(2 * np.pi * beta_freq * t)
    return alpha, beta, noise

def compute_focus_index():
    alpha, beta, noise = generate_eeg_signal()
    alpha_power = np.mean(alpha ** 2)
    beta_power = np.mean(beta ** 2)
    noise_power = np.mean(noise ** 2)
    if alpha_power == 0:
        alpha_power = 0.001
    ratio = beta_power / alpha_power
    # Normalize: higher beta/alpha ratio → higher focus
    focus_raw = np.clip(ratio * 35 + random.gauss(0, 5), 0, 100)
    return round(focus_raw, 1), round(alpha_power * 100, 2), round(beta_power * 100, 2)

def classify_focus(val):
    if val >= 65:
        return "OPTIMAL", "#00f5d4", "badge-optimal"
    elif val >= 35:
        return "MODERATE", "#ffc400", "badge-moderate"
    else:
        return "LOW", "#ff3c5a", "badge-low"

def update_bio_energy():
    # Slow drift with random walk
    delta = random.gauss(0, 2)
    st.session_state.bio_energy = float(np.clip(
        st.session_state.bio_energy + delta, 10, 100
    ))

def update_noise():
    delta = random.gauss(0, 1.5)
    st.session_state.noise_level = float(np.clip(
        st.session_state.noise_level + delta, 5, 80
    ))


# ─── Generate Focus Windows (based on history) ────────────────────────────────
def compute_focus_windows(history):
    if len(history) < 5:
        return []
    windows = []
    now = datetime.now()
    # Simulate 3 upcoming biological windows based on bio energy
    energy = st.session_state.bio_energy
    for i in range(3):
        offset_min = 15 + i * 45 + random.randint(-5, 5)
        duration = int(np.clip(energy / 10 + random.gauss(0, 2), 10, 45))
        quality = "OPTIMAL" if energy > 70 else ("MODERATE" if energy > 40 else "LOW")
        color_map = {"OPTIMAL": "#00f5d4", "MODERATE": "#ffc400", "LOW": "#ff3c5a"}
        badge_map = {"OPTIMAL": "badge-optimal", "MODERATE": "badge-moderate", "LOW": "badge-low"}
        start = now + timedelta(minutes=offset_min)
        windows.append({
            "start": start.strftime("%H:%M"),
            "duration": duration,
            "quality": quality,
            "color": color_map[quality],
            "badge": badge_map[quality],
        })
    return windows


# ─── LUNA Insight Generator ───────────────────────────────────────────────────
def luna_insight(focus, noise, energy, tasks_done):
    insights = []

    if noise > 50:
        insights.append("Neural noise is elevated. Recommend a 5-minute dopamine-reset break — step away from screens and engage in slow breathing.")
    elif noise > 30:
        insights.append("Mild neural interference detected. Reducing auditory stimulation may improve signal clarity.")
    else:
        insights.append("Neural baseline is clean. Conditions are favorable for sustained cognitive work.")

    if focus >= 65:
        insights.append(f"Focus Index is strong at {focus}. This is a prime window — allocate your highest-priority task here.")
    elif focus >= 35:
        insights.append(f"Focus is moderate ({focus}/100). Consider chunking tasks into 20-minute intervals.")
    else:
        insights.append(f"Focus Index is low ({focus}/100). Avoid decision-heavy tasks. Routine or low-demand work is advised.")

    if energy < 40:
        insights.append("Biological energy reserves are depleted. Hydration and a short physical movement break are indicated.")
    elif energy > 80:
        insights.append(f"Biological energy is high ({energy:.0f}%). Leverage this window for complex problem-solving.")

    if tasks_done > 0:
        insights.append(f"Task momentum detected: {tasks_done} item(s) completed. Reward circuitry engaged — maintain this loop.")

    return " ".join(insights)


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 10px 0;'>
        <div style='font-family:"Share Tech Mono",monospace; font-size:1.4rem; color:#00f5d4; 
                    letter-spacing:6px; text-shadow: 0 0 15px rgba(0,245,212,0.5);'>
            TOKAI
        </div>
        <div style='font-size:0.65rem; color:#5a8fa8; letter-spacing:3px; 
                    text-transform:uppercase; margin-top:4px;'>
            Neuro OS v0.9.2
        </div>
    </div>
    <hr/>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">System Control</div>', unsafe_allow_html=True)

    auto_refresh = st.toggle("Live Stream", value=st.session_state.auto_refresh)
    st.session_state.auto_refresh = auto_refresh

    refresh_interval = st.slider("Refresh Rate (s)", 1, 10, 3)

    if st.button("⟳ Manual Refresh"):
        st.rerun()

    st.markdown('<hr/>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Session Info</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style='font-family:"Share Tech Mono",monospace; font-size:0.7rem; color:#5a8fa8; line-height:2;'>
        DATE &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{datetime.now().strftime('%Y.%m.%d')}<br/>
        TIME &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{datetime.now().strftime('%H:%M:%S')}<br/>
        SAMPLES &nbsp;&nbsp;{len(st.session_state.focus_history)}<br/>
        STATUS &nbsp;&nbsp;&nbsp;ACTIVE
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr/>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">About LUNA</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.8rem; color:#5a8fa8; line-height:1.6;'>
        LUNA is Tokai's embedded neural analysis model. It synthesizes EEG stream data 
        with biological rhythms to generate adaptive cognitive recommendations.
    </div>
    """, unsafe_allow_html=True)


# ─── Main Header ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="tokai-header">
    <div>
        <div class="tokai-logo">TOKAI</div>
        <div class="tokai-subtitle">Neurosupportive Dashboard · ADHD Management System</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Generate New Data Point ──────────────────────────────────────────────────
focus_val, alpha_power, beta_power = compute_focus_index()
update_bio_energy()
update_noise()

MAX_HISTORY = 60
st.session_state.focus_history.append(focus_val)
st.session_state.timestamp_history.append(datetime.now().strftime("%H:%M:%S"))

if len(st.session_state.focus_history) > MAX_HISTORY:
    st.session_state.focus_history = st.session_state.focus_history[-MAX_HISTORY:]
    st.session_state.timestamp_history = st.session_state.timestamp_history[-MAX_HISTORY:]

focus_status, focus_color, focus_badge = classify_focus(focus_val)

# ─── KPI Row ──────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Focus Index</div>
        <div class="metric-value" style="color:{focus_color};">{focus_val}<span class="metric-unit">/100</span></div>
        <div style="margin-top:8px;"><span class="{focus_badge}">{focus_status}</span></div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Bio Energy</div>
        <div class="metric-value" style="color:#a78bfa;">{st.session_state.bio_energy:.0f}<span class="metric-unit">%</span></div>
        <div style="margin-top:8px; font-family:'Share Tech Mono',monospace; font-size:0.7rem; color:#5a8fa8;">
            {'▓' * int(st.session_state.bio_energy // 10)}{'░' * (10 - int(st.session_state.bio_energy // 10))}
        </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    noise_color = "#ff3c5a" if st.session_state.noise_level > 50 else ("#ffc400" if st.session_state.noise_level > 25 else "#00f5d4")
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Neural Noise</div>
        <div class="metric-value" style="color:{noise_color};">{st.session_state.noise_level:.0f}<span class="metric-unit">μV²</span></div>
        <div style="margin-top:8px; font-family:'Share Tech Mono',monospace; font-size:0.7rem; color:{noise_color};">
            {'HIGH' if st.session_state.noise_level > 50 else 'NOMINAL' if st.session_state.noise_level > 25 else 'CLEAR'}
        </div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    alpha_beta_ratio = round(alpha_power / beta_power if beta_power > 0 else 0, 2)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">α/β Wave Ratio</div>
        <div class="metric-value" style="color:#38bdf8;">{alpha_beta_ratio}</div>
        <div style="margin-top:8px; font-family:'Share Tech Mono',monospace; font-size:0.7rem; color:#5a8fa8;">
            α:{alpha_power:.2f} &nbsp; β:{beta_power:.2f}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# ─── Main Dashboard Columns ───────────────────────────────────────────────────
left_col, right_col = st.columns([3, 2], gap="medium")

with left_col:
    # ── Real-Time Focus Chart ─────────────────────────────────────────────────
    st.markdown('<div class="section-header">Real-Time Focus Stream</div>', unsafe_allow_html=True)

    df = pd.DataFrame({
        "Time": st.session_state.timestamp_history,
        "Focus": st.session_state.focus_history,
    })

    fig = go.Figure()

    # Fill area
    fig.add_trace(go.Scatter(
        x=df["Time"], y=df["Focus"],
        mode="lines",
        fill="tozeroy",
        fillcolor="rgba(0, 245, 212, 0.04)",
        line=dict(color="rgba(0,0,0,0)", width=0),
        showlegend=False, hoverinfo="skip",
    ))

    # Threshold zones
    fig.add_hrect(y0=65, y1=100, fillcolor="rgba(0,245,212,0.04)", line_width=0)
    fig.add_hrect(y0=35, y1=65, fillcolor="rgba(255,196,0,0.03)", line_width=0)
    fig.add_hrect(y0=0,  y1=35, fillcolor="rgba(255,60,90,0.03)", line_width=0)

    # Threshold lines
    fig.add_hline(y=65, line_dash="dot", line_color="rgba(0,245,212,0.3)", line_width=1)
    fig.add_hline(y=35, line_dash="dot", line_color="rgba(255,196,0,0.3)", line_width=1)

    # Main signal
    fig.add_trace(go.Scatter(
        x=df["Time"], y=df["Focus"],
        mode="lines+markers",
        line=dict(color="#00f5d4", width=2.5, shape="spline", smoothing=0.8),
        marker=dict(
            size=[6 if i == len(df) - 1 else 2 for i in range(len(df))],
            color=[focus_color if i == len(df) - 1 else "#00f5d4" for i in range(len(df))],
            symbol="circle",
            line=dict(width=0),
        ),
        name="Focus Index",
        hovertemplate="<b>%{x}</b><br>Focus: %{y:.1f}<extra></extra>",
    ))

    # Current value annotation
    if len(df) > 0:
        fig.add_annotation(
            x=df["Time"].iloc[-1],
            y=df["Focus"].iloc[-1],
            text=f" {focus_val}",
            showarrow=False,
            font=dict(size=13, color=focus_color, family="Share Tech Mono"),
            xanchor="left",
        )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=10, t=10, b=0),
        height=280,
        xaxis=dict(
            showgrid=False, zeroline=False,
            tickfont=dict(color="#5a8fa8", size=9, family="Share Tech Mono"),
            showticklabels=len(df) > 0,
            nticks=8,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(0,245,212,0.06)",
            zeroline=False,
            range=[0, 105],
            tickfont=dict(color="#5a8fa8", size=9, family="Share Tech Mono"),
            ticksuffix=" ",
        ),
        showlegend=False,
        hovermode="x unified",
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ── Focus Window Predictor ────────────────────────────────────────────────
    st.markdown('<div class="section-header">Optimal Focus Window Predictor</div>', unsafe_allow_html=True)
    windows = compute_focus_windows(st.session_state.focus_history)

    if not windows:
        st.markdown("""
        <div style='color:#5a8fa8; font-family:"Share Tech Mono",monospace; font-size:0.8rem; 
                    text-align:center; padding:20px;'>
            Collecting baseline data... stream more samples.
        </div>
        """, unsafe_allow_html=True)
    else:
        for i, w in enumerate(windows):
            st.markdown(f"""
            <div class="focus-window">
                <div>
                    <div style='font-family:"Share Tech Mono",monospace; font-size:0.65rem; 
                                color:#5a8fa8; letter-spacing:2px;'>WINDOW {i+1}</div>
                    <div style='font-size:1.1rem; color:#c8d8e8; font-weight:600; margin-top:2px;'>
                        {w['start']} &nbsp;·&nbsp; {w['duration']} min
                    </div>
                </div>
                <div style='text-align:right;'>
                    <span class='{w["badge"]}'>{w["quality"]}</span>
                    <div style='font-family:"Share Tech Mono",monospace; font-size:0.65rem; 
                                color:#5a8fa8; margin-top:6px;'>
                        Energy: {st.session_state.bio_energy:.0f}%
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

with right_col:
    # ── LUNA AI Insights ──────────────────────────────────────────────────────
    st.markdown('<div class="section-header">LUNA · Neural Insights</div>', unsafe_allow_html=True)

    tasks_done = sum(1 for t in st.session_state.tasks if t["done"])
    luna_text = luna_insight(focus_val, st.session_state.noise_level,
                             st.session_state.bio_energy, tasks_done)

    st.markdown(f"""
    <div class="luna-panel">
        <div class="luna-id">◈ LUNA MODEL · ADAPTIVE RESPONSE</div>
        <div class="luna-text">"{luna_text}"</div>
        <div style='margin-top:14px; font-family:"Share Tech Mono",monospace; font-size:0.65rem; 
                    color:#1a3a5c; text-align:right;'>
            {datetime.now().strftime('%H:%M:%S')} · CONFIDENCE 87%
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Alpha/Beta Wave Breakdown ─────────────────────────────────────────────
    st.markdown('<div class="section-header">Wave Breakdown</div>', unsafe_allow_html=True)

    wave_fig = go.Figure()
    wave_fig.add_trace(go.Bar(
        x=["Alpha (8-13 Hz)", "Beta (13-30 Hz)"],
        y=[alpha_power, beta_power],
        marker_color=["rgba(0,245,212,0.7)", "rgba(0,102,255,0.7)"],
        marker_line=dict(color=["#00f5d4", "#0066ff"], width=1),
        width=0.4,
    ))
    wave_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=10, b=0),
        height=160,
        xaxis=dict(
            showgrid=False, zeroline=False,
            tickfont=dict(color="#5a8fa8", size=9, family="Share Tech Mono"),
        ),
        yaxis=dict(
            showgrid=True, gridcolor="rgba(0,245,212,0.06)",
            zeroline=False,
            tickfont=dict(color="#5a8fa8", size=9, family="Share Tech Mono"),
        ),
        showlegend=False,
    )
    st.plotly_chart(wave_fig, use_container_width=True, config={"displayModeBar": False})

    # ── Task Manager ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Task Integration</div>', unsafe_allow_html=True)

    new_task = st.text_input("", placeholder="Add a task and press Enter...", key="task_input", label_visibility="collapsed")
    if new_task:
        st.session_state.tasks.append({"text": new_task, "done": False})
        st.rerun()

    for i, task in enumerate(st.session_state.tasks):
        cols = st.columns([0.08, 0.82, 0.1])
        with cols[0]:
            checked = st.checkbox("", value=task["done"], key=f"task_{i}", label_visibility="collapsed")
            st.session_state.tasks[i]["done"] = checked
        with cols[1]:
            style_class = "todo-done" if task["done"] else ""
            st.markdown(f"""
            <div class="todo-item {style_class}" style="margin-bottom:0; padding:6px 10px;">
                {task["text"]}
            </div>
            """, unsafe_allow_html=True)
        with cols[2]:
            if st.button("✕", key=f"del_{i}", help="Remove task"):
                st.session_state.tasks.pop(i)
                st.rerun()

    if st.session_state.tasks:
        done_count = sum(1 for t in st.session_state.tasks if t["done"])
        pct = int(done_count / len(st.session_state.tasks) * 100)
        st.markdown(f"""
        <div style='margin-top:10px; font-family:"Share Tech Mono",monospace; 
                    font-size:0.7rem; color:#5a8fa8;'>
            PROGRESS &nbsp;{done_count}/{len(st.session_state.tasks)} &nbsp;
            <span style='color:#00f5d4;'>{pct}%</span>
        </div>
        """, unsafe_allow_html=True)

# ─── Auto-Refresh ─────────────────────────────────────────────────────────────
if st.session_state.auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()
