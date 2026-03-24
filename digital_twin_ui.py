import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt

st.set_page_config(page_title="Digital Twin Pro", layout="wide")

st.title("🏭 Digital Twin - KEDA Polishing Line (Pro Version)")

# --------------------------
# CONTROL PANEL (ALL SLIDERS)
# --------------------------
st.sidebar.header("⚙️ Full Process Control Panel")

# Production
speed = st.sidebar.slider("Line Speed (m/min)", 10, 20, 15)
tile_size = st.sidebar.slider("Tile Size (mm)", 600, 1200, 800)
efficiency = st.sidebar.slider("Efficiency (%)", 50, 100, 85)

# Mechanical
pressure = st.sidebar.slider("Pressure (MPa)", 0.5, 0.9, 0.7)
rpm = st.sidebar.slider("RPM", 300, 1500, 800)
load_factor = st.sidebar.slider("Load (%)", 50, 120, 100)
vibration = st.sidebar.slider("Vibration (%)", 0, 100, 20)
bearing_temp = st.sidebar.slider("Bearing Temp (°C)", 30, 120, 60)

# Process
water_flow = st.sidebar.slider("Water Flow (%)", 50, 120, 100)
slurry = st.sidebar.slider("Slurry (%)", 50, 120, 100)
abrasive = st.sidebar.slider("Abrasive (%)", 50, 120, 100)
tile_hardness = st.sidebar.slider("Tile Hardness (%)", 50, 120, 100)
moisture = st.sidebar.slider("Moisture (%)", 0, 10, 3)

# Energy
idle_loss = st.sidebar.slider("Idle Loss (%)", 0, 30, 10)

# Quality
target_gloss = st.sidebar.slider("Target Gloss", 70, 100, 90)
rejection = st.sidebar.slider("Rejection (%)", 0, 20, 5)

# --------------------------
# DATA GENERATION
# --------------------------
data = []

for t in range(20):
    speed_var = speed + random.uniform(-1, 1)
    pressure_var = pressure + random.uniform(-0.05, 0.05)

    heads = [random.uniform(7, 12) for _ in range(8)]

    production = speed_var * 60 * (efficiency/100)

    power = sum(heads) * (load_factor/100) * (1 + vibration/100)

    sec = power / production

    gloss = 95 \
            - pressure_var * 20 \
            - (1 - abrasive/100) * 10 \
            + water_flow * 0.03 \
            - moisture * 1.5

    data.append({
        "time": t,
        "speed": speed_var,
        "power": power,
        "production": production,
        "sec": sec,
        "gloss": gloss
    })

df = pd.DataFrame(data)
last = df.iloc[-1]

# --------------------------
# KPI
# --------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Production", f"{last['production']:.0f}")
col2.metric("Power", f"{last['power']:.0f}")
col3.metric("SEC", f"{last['sec']:.3f}")
col4.metric("Gloss", f"{last['gloss']:.1f}")

# --------------------------
# ALERTS
# --------------------------
st.subheader("🚨 Alerts")

if pressure > 0.8:
    st.error("High Pressure")

if vibration > 70:
    st.error("High Vibration")

if last["gloss"] < 80:
    st.warning("Low Gloss")

# --------------------------
# GRAPH
# --------------------------
st.subheader("📈 Trends")

fig, ax = plt.subplots(3, 1, figsize=(8, 6))

ax[0].plot(df["time"], df["speed"])
ax[0].set_title("Speed")

ax[1].plot(df["time"], df["power"])
ax[1].set_title("Power")

ax[2].plot(df["time"], df["gloss"])
ax[2].set_title("Gloss")

st.pyplot(fig)
