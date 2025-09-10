import streamlit as st
import pandas as pd
import random
import datetime
import matplotlib.pyplot as plt

st.markdown("<h1 style='text-align:center; font-size:48px;'>💧 Water Quality Dashboard</h1>", unsafe_allow_html=True)

# Generate fake sensor data
def generate_data(num_readings=50):
    values = [random.randint(50, 600) for _ in range(num_readings)]
    timestamps = [datetime.datetime.now() - datetime.timedelta(minutes=5*i) for i in range(num_readings)]
    df = pd.DataFrame({"Time": timestamps, "Microplastics": values})
    df = df.sort_values("Time")
    return df

data = generate_data()

# Threshold sliders
good_threshold = st.sidebar.slider("Good max microplastics", 0, 600, 200)
moderate_threshold = st.sidebar.slider("Moderate max microplastics", 0, 600, 400)

# Assign status
def get_status(v):
    if v < good_threshold:
        return "Good"
    elif v < moderate_threshold:
        return "Moderate"
    else:
        return "Contaminated"

data["Status"] = data["Microplastics"].apply(get_status)

# Latest reading and status
latest_value = data["Microplastics"].iloc[-1]
latest_status = get_status(latest_value)

# Decide Safe or Unsafe
if latest_status in ["Good", "Moderate"]:
    display_status = "Safe"
    bg_color = "green"
else:
    display_status = "Unsafe"
    bg_color = "red"

# 🔹 Make status card bigger
st.markdown(
    f"""
    <div style="background-color:{bg_color};
                padding:40px;
                border-radius:20px;
                text-align:center;
                margin-bottom:30px;">
        <h1 style="color:white; font-size:50px; margin:0;">Latest Water Status: {display_status}</h1>
        <h2 style="color:white; font-size:40px; margin:10px 0 0;">Microplastic Reading: {latest_value}</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# Infographic style pie chart for status distribution
status_counts = data["Status"].value_counts()
sizes = status_counts.values
labels = status_counts.index
colors = {"Good": "green", "Moderate": "orange", "Contaminated": "red"}
color_map = [colors[label] for label in labels]

fig1, ax1 = plt.subplots()
explode = [0.05] * len(sizes)
ax1.pie(
    sizes,
    explode=explode,
    labels=labels,
    colors=color_map,
    autopct='%1.1f%%',
    shadow=True,
    startangle=90,
    wedgeprops=dict(edgecolor='w'),
    textprops=dict(color="black", fontsize=12)
)
ax1.set(aspect="equal", title="Water Quality Status Distribution")

# Plot area chart for microplastic levels over time
fig2, ax2 = plt.subplots()
ax2.fill_between(data['Time'], data['Microplastics'], color='skyblue', alpha=0.5)
ax2.plot(data['Time'], data['Microplastics'], color='SteelBlue')
ax2.axhline(y=good_threshold, color='green', linestyle='--', label='Good Threshold')
ax2.axhline(y=moderate_threshold, color='orange', linestyle='--', label='Moderate Threshold')
ax2.set_xlabel('Time')
ax2.set_ylabel('Microplastic Level')
ax2.set_title('Microplastic Levels Over Time')
ax2.legend()
plt.xticks(rotation=45)

# Display both charts
col1, col2 = st.columns(2)
with col1:
    st.pyplot(fig1)
with col2:
    st.pyplot(fig2)
