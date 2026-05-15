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
def calculate_inr(oil, trade, gold_res, fii):
    # The new 'floor' as of today's market opening
    base_inr = 95.94 
    
    # 1. Oil Price Impact: 
    # Current Brent is ~$107. Every $1 move now has a higher 
    # psychological impact on the Rupee compared to when it was $80.
    oil_impact = (oil - 107) * 0.08 
    
    # 2. Trade Balance Impact: 
    # India's monthly deficit is widening toward $25B-$30B.
    trade_impact = (trade + 25) * -0.20 
    
    # 3. Gold Reserves: 
    # RBI reserves have dipped to ~$691B. Gold acts as a buffer.
    gold_impact = (gold_res - 45) * -0.03 
    
    # 4. FII Flows (The 'Panic' Button): 
    # Sustained selling of ~Rs 2 lakh crore. Inflows are rare now.
    fii_impact = fii * -0.45 
    
    final_inr = base_inr + oil_impact + trade_impact + gold_impact + fii_impact
    return round(final_inr, 2)

# --- UPDATED INPUTS (Sidebar) ---
st.sidebar.header("Real-Time Factors (May 2026)")

# Set defaults to today's actual market rates
oil_price = st.sidebar.slider("Brent Crude (USD/Barrel)", 80, 140, 107)
trade_balance = st.sidebar.slider("Trade Deficit (USD Billion)", -50, 0, -25)
gold_reserves = st.sidebar.slider("Gold Reserves Value (USD Billion)", 30, 80, 48)
fii_flow = st.sidebar.slider("Net FII Flow (USD Billion)", -15, 5, -2)

current_val = calculate_inr(oil_price, trade_balance, gold_reserves, fii_flow)

# --- PHENOMENON ALERTS ---
if oil_price > 110:
    st.toast("🚨 Energy Crisis: Oil above $110 signals potential fuel price hikes and 'Imported Inflation' for India.", icon="🔥")
if fii_flow < -5:
    st.toast("📉 Capital Flight: Aggressive FII selling is overwhelming the RBI's ability to intervene.", icon="💸")
if current_val > 98:
    st.error("⚠️ Critical Level: Rupee approaching the psychological 100-mark. Market expects a Repo Rate hike.")

# --- DISPLAY (Metric & Gauge) ---
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

# --- DEPENDENCY SECTION ---
st.divider()
st.subheader("The Correlation Matrix")
st.write("""
- **Oil vs Trade:** As Oil prices rise, the 'Trade Balance' will naturally slide further into a deficit because India imports 85% of its oil.
- **Gold vs INR:** Gold reserves act as a 'Safe Haven'. During global volatility, higher gold reserves prevent a free-fall of the Rupee.
""")
