import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Mining Predictive Maintenance", layout="wide")

st.title("🚜 Mining Equipment Health Monitor")
st.markdown("Real-time sensor telemetry for predictive maintenance.")


@st.cache_data
def load_mining_data():
    df = pd.read_csv('predictive_maintenance.csv')
    return df

df = load_mining_data()


st.sidebar.header("Filter by Machine Type")
m_type = st.sidebar.multiselect("Select Grade:", options=df['Type'].unique(), default=df['Type'].unique())
filtered_df = df[df['Type'].isin(m_type)]


avg_temp = filtered_df['Process temperature [K]'].mean()
failure_count = filtered_df['Target'].sum()

col1, col2 = st.columns(2)
col1.metric("Average Process Temp", f"{avg_temp:.2f} K")
col2.metric("Total Failures Detected", failure_count, delta="-5% vs Last Month", delta_color="inverse")


st.subheader("Torque vs. Rotational Speed (Failure Clusters)")
fig = px.scatter(filtered_df, x="Rotational speed [rpm]", y="Torque [Nm]", 
                 color="Target", hover_data=['UDI'],
                 title="Failure Points in Torque/Speed Spectrum")
st.plotly_chart(fig, width='stretch')

st.subheader("Temperature Distribution")
fig2 = px.histogram(filtered_df, x="Air temperature [K]", color="Target", barmode="overlay")
st.plotly_chart(fig2, width='stretch')


st.subheader("🚨 High-Risk Equipment Watchlist")
high_risk = filtered_df[filtered_df['Target'] == 1].tail(10)
st.table(high_risk[['UDI', 'Product ID', 'Air temperature [K]', 'Torque [Nm]']])