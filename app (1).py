import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Crop Yield Dashboard", layout="wide")

st.title("🌾 Smart Farming Crop Yield Dashboard")
st.markdown("Interactive visualization of crop yield and environmental factors.")

@st.cache_data
def load_data():
    return pd.read_csv("Smart_Farming_Crop_Yield_2024_preprocessed.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Region",
    sorted(df["region"].unique()),
    default=list(df["region"].unique())
)

crop = st.sidebar.multiselect(
    "Crop Type",
    sorted(df["crop_type"].unique()),
    default=list(df["crop_type"].unique())
)

disease = st.sidebar.multiselect(
    "Disease Status",
    sorted(df["crop_disease_status"].unique()),
    default=list(df["crop_disease_status"].unique())
)

filtered = df[
    (df["region"].isin(region)) &
    (df["crop_type"].isin(crop)) &
    (df["crop_disease_status"].isin(disease))
]

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Records", len(filtered))
col2.metric("Avg Yield", f"{filtered['yield_kg_per_hectare'].mean():.2f}")
col3.metric("Max Yield", f"{filtered['yield_kg_per_hectare'].max():.2f}")
col4.metric("Min Yield", f"{filtered['yield_kg_per_hectare'].min():.2f}")

# Yield Distribution
st.subheader("Yield Distribution")
fig1 = px.histogram(filtered, x="yield_kg_per_hectare", nbins=30)
st.plotly_chart(fig1, use_container_width=True)

# NDVI vs Yield
st.subheader("NDVI vs Yield")
fig2 = px.scatter(
    filtered,
    x="NDVI_index",
    y="yield_kg_per_hectare",
    color="crop_type",
    opacity=0.7
)
st.plotly_chart(fig2, use_container_width=True)

# Rainfall vs Yield
st.subheader("Rainfall vs Yield")
fig3 = px.scatter(
    filtered,
    x="rainfall_mm",
    y="yield_kg_per_hectare",
    color="crop_type",
    trendline="lowess"
)
st.plotly_chart(fig3, use_container_width=True)

# Temporal Analysis
st.subheader("Yield vs Sowing Month")
fig4 = px.box(filtered, x="sowing_month", y="yield_kg_per_hectare")
st.plotly_chart(fig4, use_container_width=True)

# Geospatial
st.subheader("Geospatial Yield Distribution")
fig5 = px.scatter_geo(
    filtered,
    lat="latitude",
    lon="longitude",
    color="yield_kg_per_hectare",
    color_continuous_scale="Viridis"
)
st.plotly_chart(fig5, use_container_width=True)
