import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt

st.set_page_config(page_title="Digital Twin", layout="wide")

st.title("🏭 Digital Twin - KEDA Polishing Line")

# --------------------------
# CONTROL PANEL
# --------------------------
st.sidebar.header("⚙️ Process Control Panel")

speed = st.sidebar.slider("Line Speed (m/min)", 10, 20, 15)
pressure = st.sidebar.slider("Pressure (MPa)", 0.5, 0.9, 0.7)
abrasive = st.sidebar.slider("Abrasive Condition (%)", 50, 120, 100)
water_flow = st.sidebar.slider("Water Flow (%)", 50, 120, 100)
vibration = st.sidebar.slider("Vibration (%)", 0, 100, 20)

# --------------------------
# DATA GENERATION
# --------------------------
data = []

for t in range(20):
    speed_var = speed + random.uniform(-1, 1)
    pressure_var = pressure + random.uniform(-0.05, 0.05)

    heads = [random.uniform(7, 12) for _ in range(8)]

    production = speed_var * 60
    power = sum(heads) * (1 + vibration/100)
    sec = power / production

    gloss = 95 - pressure_var * 20 - (1 - abrasive/100) * 10 + water_flow * 0.03

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
# GRAPHS
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
