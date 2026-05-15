import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- CONFIGURATION ---
st.set_page_config(page_title="INR Value Simulator", layout="wide")

st.title("📊 Indian Rupee (INR) Value Predictor")
st.markdown("""
This dashboard simulates how the Indian Rupee reacts to global and domestic economic shifts. 
Adjust the sliders in the sidebar to see the impact.
""")

# --- SIDEBAR / INPUTS ---
st.sidebar.header("Economic Parameters")

# 1. Crude Oil Price (Brent)
oil_price = st.sidebar.slider("Crude Oil Price (USD/Barrel)", 40, 150, 85)

# 2. Trade Balance (Exports - Imports)
# We calculate this as a net figure in USD Billions
trade_balance = st.sidebar.slider("Monthly Trade Balance (USD Billion)", -40, 5, -20)

# 3. Gold Reserves
gold_reserves = st.sidebar.slider("Gold Reserves (USD Billion)", 30, 100, 45)

# 4. FII Inflow (Extra Variable: Foreign Investment is crucial)
fii_flow = st.sidebar.slider("FII Net Inflow (USD Billion)", -10, 10, 1)

# --- LOGIC ENGINE ---
def calculate_inr(oil, trade, gold, fii):
    base_inr = 83.50
    
    # Logic 1: Oil Price Impact
    # Rule: Every $10 rise in oil typically depreciates Rupee by ~40-60 paise
    oil_impact = (oil - 85) * 0.05
    
    # Logic 2: Trade Balance Impact
    # Rule: Widening deficit (negative) weakens Rupee
    trade_impact = (trade + 20) * -0.15
    
    # Logic 3: Gold Reserves
    # Rule: Higher reserves provide a buffer (Appreciation)
    gold_impact = (gold - 45) * -0.02
    
    # Logic 4: FII Flows
    # Rule: Outflows (Negative) weaken the Rupee significantly
    fii_impact = fii * -0.30
    
    final_inr = base_inr + oil_impact + trade_impact + gold_impact + fii_impact
    return round(final_inr, 2)

current_val = calculate_inr(oil_price, trade_balance, gold_reserves, fii_flow)

# --- POP-UP / PHENOMENON EXPLANATION ---
if oil_price > 100:
    st.toast("⚠️ High Oil Prices: India's high import dependency causes a 'Dollar drain', weakening the Rupee.", icon="⛽")
if trade_balance < -30:
    st.toast("🚨 Trade Deficit: We are spending more foreign currency than earning. High Rupee supply = Lower Value.", icon="📉")
if fii_flow < 0:
    st.toast("💸 Capital Flight: Foreigners are selling Indian stocks. This creates immediate Rupee depreciation.", icon="🏦")

# --- MAIN DISPLAY ---
col1, col2 = st.columns([1, 1])

with col1:
    st.metric(label="Estimated USD/INR Exchange Rate", value=f"₹{current_val}")
    
    # Visualization: Gauge Chart
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = current_val,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Rupee Strength"},
        gauge = {
            'axis': {'range': [70, 100]},
            'bar': {'color': "darkblue"},
            'steps' : [
                {'range': [70, 80], 'color': "lightgreen"},
                {'range': [80, 90], 'color': "yellow"},
                {'range': [90, 100], 'color': "red"}],
        }
    ))
    st.plotly_chart(fig)

with col2:
    st.subheader("Factor Breakdown")
    data = {
        "Factor": ["Oil Price", "Trade Balance", "Gold Reserves", "Foreign Investment (FII)"],
        "Current Setting": [f"${oil_price}", f"${trade_balance}B", f"${gold_reserves}B", f"${fii_flow}B"],
        "Impact on Rupee": [
            "Negative (Depreciation)" if oil_price > 85 else "Positive",
            "Negative" if trade_balance < -20 else "Positive",
            "Positive (Buffer)" if gold_reserves > 45 else "Neutral",
            "Positive" if fii_flow > 0 else "Negative"
        ]
    }
    st.table(pd.DataFrame(data))

# --- DEPENDENCY SECTION ---
st.divider()
st.subheader("The Correlation Matrix")
st.write("""
- **Oil vs Trade:** As Oil prices rise, the 'Trade Balance' will naturally slide further into a deficit because India imports 85% of its oil.
- **Gold vs INR:** Gold reserves act as a 'Safe Haven'. During global volatility, higher gold reserves prevent a free-fall of the Rupee.
""")