import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Importing the data
@st.cache_data
def load_data():
    df = pd.read_csv("pre-processed_data.csv")
    ext = pd.read_csv("external_data.csv")
    return df, ext

df, ext = load_data()

# Set page title
st.title("Bike Traffic Analysis in Paris")

# Sidebar

# Set date to datetime format
df["date"] = pd.to_datetime(df["date"])

st.sidebar.header("Custom Options")
analysis_type = st.sidebar.selectbox(
    "Choose analysis type:",
    ("Bike Traffic Heatmap", "Weather Analysis", "Lockdown & Curfew Analysis", "Holiday Analysis", "Sunlight Analysis", "Rush Hour Analysis")
)

df["month_year"] = df['date'].dt.strftime('%B %Y')
month = st.sidebar.selectbox("Select month", df["month_year"].unique())

# Display header based on the analysis type selected
st.header(f"{analysis_type} in {month}")

# Function to plot Kernel Density Estimates for specific conditions
def plot_kde(df, column, values, labels, colors, title):
    fig, ax = plt.subplots(figsize=(11, 6))
    for value, label, color in zip(values, labels, colors):
        sns.kdeplot(
            df[df[column] == value]['log_bike_count'],
            color=color, label=label, fill=True
        )
    ax.set_xlabel('Log Bike Count')
    ax.set_ylabel('Density')
    ax.set_title(title)
    ax.legend()
    st.pyplot(fig)

if analysis_type == "Bike Traffic Heatmap":
    df_map = df[df['month_year'] == month]
    df_map = df.drop(df.columns.difference(["bike_count", "latitude", "longitude", "site_name"]), axis=1)
    df_map["half_bike_count"] = 0.5*df_map["bike_count"]
    st.map(data=df_map, latitude="latitude", longitude="longitude", size="half_bike_count", color="#0000ff")

elif analysis_type == "Lockdown & Curfew Analysis":
    df1 = df[df["date"] == month]
    st.subheader("Lockdown vs Curfew Kernel Density Plot")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Lockdown KDE
    sns.kdeplot(
        df1[df1['Lockdown'] == 1]['log_bike_count'],
        color='blue', label='Lockdown', fill=True, ax=axes[0]
    )
    sns.kdeplot(
        df1[df1['Lockdown'] == 0]['log_bike_count'],
        color='red', label='No Lockdown', fill=True, ax=axes[0]
    )
    axes[0].set_title('Kernel Density for Lockdown')
    
    # Curfew KDE
    sns.kdeplot(
        df1[df1['Curfew'] == 1]['log_bike_count'],
        color='green', label='Curfew', fill=True, ax=axes[1]
    )
    sns.kdeplot(
        df1[df1['Curfew'] == 0]['log_bike_count'],
        color=sns.color_palette('Blues')[4], label='No Curfew', fill=True, ax=axes[1]
    )
    axes[1].set_title('Kernel Density for Curfew')
    
    fig.legend(loc='upper right', bbox_to_anchor=(1.15, 0.95))
    plt.tight_layout()
    st.pyplot(fig)

elif analysis_type == "Holiday Analysis":
    df1 = df[df["date"] == month]
    st.subheader("Holiday vs Non-Holiday Kernel Density Plot")
    plot_kde(
        df1, 'Holiday',
        [0, 1],
        ['No Holiday', 'Holiday'],
        ['blue', 'red'],
        'Log Bike Count Histogram Density by Holiday'
    )

elif analysis_type == "Sunlight Analysis":
    df1 = df[df["date"] == month]
    st.subheader("Daylight vs Darkness Kernel Density Plot")
    plot_kde(
        df1, 'Sun',
        [0, 1],
        ['Dark', 'Daylight'],
        ['blue', 'red'],
        'Log Bike Count Histogram Density by Sunlight'
    )

elif analysis_type == "Rush Hour Analysis":
    df1 = df[df["date"] == month]
    st.subheader("Rush Hour Kernel Density Plot")
    plot_kde(
        df1, 'rush_hour',
        [0, 1],
        ['Non-Rush Hour', 'Rush Hour'],
        ['blue', 'red'],
        'Log Bike Count Histogram Density by Rush Hour'
    )

elif "Weather Analysis":
    df1 = df[df["date"] == month]
    st.subheader("Weather Condition Kernel Density Plot")
    plot_kde(
        df1, 'weather_condition',
        ['No Precipitation', 'Rain'],
        ['No Precipitation', 'Rain'],
        ['blue', 'red'],
        'Log Bike Count Histogram Density by Weather Condition'
    )
    
# Weekly bike traffic trends
st.header("Weekly Bike Traffic Trend")
plt.figure(figsize=(12, 8))
plt.plot(df[["date", "bike_count"]].set_index("date").resample("W").mean())
plt.title("Weekly Mean Bike Traffic")
plt.xlabel("Date")
plt.ylabel("Bike Count")
st.pyplot(plt)