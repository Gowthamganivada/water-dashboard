import streamlit as st
import pandas as pd
import random
import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="Water Quality Dashboard", layout="wide")
st.title("        💧 Water Quality Dashboard ")

# Generate fake sensor data
def generate_data(num_readings=50):
    values = [random.randint(50, 600) for _ in range(num_readings)]
    timestamps = [datetime.datetime.now() - datetime.timedelta(minutes=5*i) for i in range(num_readings)]
    df = pd.DataFrame({"Time": timestamps, "Microplastics": values})
    df = df.sort_values("Time")
    return df

data = generate_data()

# Threshold sliders for live adjustment
good_threshold = st.sidebar.slider("Good max microplastics", 0, 600, 200)
moderate_threshold = st.sidebar.slider("Moderate max microplastics", 0, 600, 400)

def get_status(v):
    if v < good_threshold:
        return "Good"
    elif v < moderate_threshold:
        return "Moderate"
    else:
        return "Contaminated"

data["Status"] = data["Microplastics"].apply(get_status)
latest_value = data["Microplastics"].iloc[-1]
latest_status = get_status(latest_value)
latest_time = data["Time"].iloc[-1].strftime('%Y-%m-%d %H:%M:%S')

# Decide Safe or Unsafe and set color
if latest_status in ["Good", "Moderate"]:
    display_status = latest_status
    bg_color = "#34a853" if latest_status == "Good" else "#ffa500"
else:
    display_status = "Unsafe"
    bg_color = "#ea4335"

# Show Latest Status Box
st.markdown(
    f"""
    <div style="background-color:{bg_color};padding:15px 5px 15px 5px;border-radius:10px;text-align:center;">
        <span style="font-size:22px;font-weight:bold;color:white;">⭐ Latest Water Status: {display_status}</span><br>
        <span style="font-size:18px;color:white;">Latest Microplastic Reading: <b>{latest_value}</b></span><br>
        <span style="font-size:14px;color:white;">Timestamp: {latest_time}</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("") # Space

# Pie chart for status distribution
status_counts = data["Status"].value_counts()
sizes = status_counts.values
labels = status_counts.index
colors = {"Good": "#34a853", "Moderate": "#ffa500", "Contaminated": "#ea4335"}
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
    wedgeprops=dict(edgecolor='white', linewidth=2),
    textprops=dict(color="black", fontsize=12, fontweight='bold')
)
ax1.set(aspect="equal", title="Water Quality Status Distribution")

# Area chart for microplastic levels over time
fig2, ax2 = plt.subplots()
ax2.fill_between(data['Time'], data['Microplastics'], color='skyblue', alpha=0.5)
ax2.plot(data['Time'], data['Microplastics'], color='SteelBlue', linewidth=2)
ax2.axhline(y=good_threshold, color="#34a853", linestyle='--', linewidth=2, label='Good Threshold')
ax2.axhline(y=moderate_threshold, color="#ffa500", linestyle='--', linewidth=2, label='Moderate Threshold')
ax2.set_xlabel('Time', fontsize=12, fontweight="bold")
ax2.set_ylabel('Microplastic Level', fontsize=12, fontweight="bold")
ax2.set_title('Microplastic Levels Over Time', fontsize=14, fontweight="bold")
ax2.legend()
plt.xticks(rotation=45)

col1, col2 = st.columns([1,1])
with col1:
    st.pyplot(fig1)
with col2:
    st.pyplot(fig2)