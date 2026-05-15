import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURATION ---
st.set_page_config(page_title="INR Value Simulator", layout="wide")

st.title("Indian Rupee (INR) Value Predictor")
st.markdown("""
This dashboard simulates how the Indian Rupee reacts to global and domestic economic shifts. 
Adjust the sliders in the sidebar to see the impact.
""")

# --- CALIBRATED LOGIC FOR MAY 15, 2026 ---
def calculate_inr(oil, trade, gold, fii):
    base_inr = 95.94 
    oil_impact = (oil - 106) * 0.05
    trade_impact = (trade + 33) * -0.10  # Calibrated for larger deficit values
    gold_impact = (gold - 115) * -0.01 
    fii_impact = (fii + 17) * -0.15      # Calibrated for larger outflow values
    
    return round(base_inr + oil_impact + trade_impact + gold_impact + fii_impact, 2)

# --- UPDATED INPUTS (Sidebar) ---
st.sidebar.header("Real-Time Factors (May 2026)")

# Brent Crude: Range widened to account for recent $126 peak
oil_price = st.sidebar.slider("Brent Crude (USD/Barrel)", 60, 150, 106)

# Trade Deficit: Monthly values are now much higher than $25B
trade_balance = st.sidebar.slider("Monthly Trade Deficit (USD Billion)", -60, 0, -33)

# Gold Reserves: Now valued at over $100B due to high gold prices
gold_reserves = st.sidebar.slider("Gold Reserves (USD Billion)", 50, 150, 115)

# Net FII Flow: Monthly outflows have crossed $10B-$15B in crash months
fii_flow = st.sidebar.slider("Monthly Net FII Flow (USD Billion)", -25, 10, -17)
current_val = calculate_inr(oil_price, trade_balance, gold_reserves, fii_flow)

# --- PHENOMENON ALERTS ---
if oil_price > 110:
    st.toast("🚨 Energy Crisis: Oil above $110 signals potential fuel price hikes and 'Imported Inflation' for India.", icon="🔥")
if fii_flow < -5:
    st.toast("📉 Capital Flight: Aggressive FII selling is overwhelming the RBI's ability to intervene.", icon="💸")
if current_val > 98:
    st.error("⚠️ Critical Level: Rupee approaching the psychological 100-mark. Market expects a Repo Rate hike.")

# --- DISPLAY (Metric & Gauge) ---
col1, col2 = st.columns([1, 1])
with col1:
    st.metric(label="Simulated USD/INR Exchange Rate", value=f"₹{current_val}")
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = current_val,
        gauge = {
            'axis': {'range': [90, 105]}, # Shifted range up to reflect current crisis
            'steps' : [
                {'range': [90, 94], 'color': "lightgreen"},
                {'range': [94, 97], 'color': "orange"},
                {'range': [97, 105], 'color': "red"}],
            'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': 95.94}
        }
    ))
    st.plotly_chart(fig)

with col2:
    st.subheader("Factor Breakdown")
    
    # Logic calibrated for May 2026 crisis environment
    data = {
        "Factor": [
            "Brent Crude Price", 
            "Trade Balance", 
            "Gold Reserves", 
            "FII Flows"
        ],
        "Current Setting": [
            f"${oil_price}/bbl", 
            f"${trade_balance}B", 
            f"${gold_reserves}B", 
            f"${fii_flow}B"
        ],
        "Market Impact": [
            "Negative (Depreciation)" if oil_price > 107 else "Positive/Stable",
            "Negative (Drain)" if trade_balance < -25 else "Within Norms",
            "Positive (Buffer)" if gold_reserves > 48 else "Low Buffer",
            "Positive (Inflow)" if fii_flow > 0 else "Negative (Outflow)"
        ]
    }
    st.table(pd.DataFrame(data))
    
    st.info(f"""
    **Current Analysis:** 
    The Rupee is currently benchmarked at a base of **₹95.94**. 
    At this level, market sensitivity is 2.5x higher than historical averages.
    """)

# --- DEPENDENCY SECTION ---
st.divider()
st.subheader("The Correlation Matrix")
st.write("""
- **Oil vs Trade:** As Oil prices rise, the 'Trade Balance' will naturally slide further into a deficit because India imports 85% of its oil.
- **Gold vs INR:** Gold reserves act as a 'Safe Haven'. During global volatility, higher gold reserves prevent a free-fall of the Rupee.
""")
