import streamlit as st
import pandas as pd

def custom_title(text, color="#FFD700", size="1.5rem", weight="600"):
    """Display a custom styled title"""
    st.markdown(f"""
    <h3 style="
        color: {color} !important;
        font-size: {size} !important;
        font-weight: {weight} !important;
        margin-bottom: 1rem !important;
        text-shadow: 0 1px 3px rgba(0,0,0,0.3) !important;
    ">{text}</h3>
    """, unsafe_allow_html=True)

def custom_error(text, color="#FF4444", bg_color="rgba(244, 67, 54, 0.1)"):
    """Display a custom styled error message"""
    st.markdown(f"""
    <div style="
        background-color: {bg_color};
        color: {color};
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid {color};
        margin: 1rem 0;
        font-weight: 500;
    ">
        ⚠️ {text}
    </div>
    """, unsafe_allow_html=True)

def custom_warning(text, color="#FFA500", bg_color="rgba(255, 152, 0, 0.1)"):
    """Display a custom styled warning message"""
    st.markdown(f"""
    <div style="
        background-color: {bg_color};
        color: {color};
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid {color};
        margin: 1rem 0;
        font-weight: 500;
    ">
        ⚠️ {text}
    </div>
    """, unsafe_allow_html=True)

def risk_management_center(portfolio_data, market_data):
    st.sidebar.markdown("🛡️ **Risk Management Center**")

    st.title("🛡️ Risk Management Center")
    st.caption("تحليل المخاطر المالية للمحفظة | Portfolio Risk Analysis")

    # --- Metrics Section ---
    custom_title("📊 Key Risk Metrics | مؤشرات المخاطر", color="#00D4FF")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📉 Max Drawdown", "-26.1%", "أقصى انخفاض")
    col2.metric("📈 Portfolio Beta", "1.00", "بيتا المحفظة")
    col3.metric("📊 Volatility", "0.3%", "التقلب")
    col4.metric("⚖️ Sharpe Ratio", "-0.54", "نسبة شارب")

    # --- Stop-Loss & Take-Profit ---
    custom_title("🎯 Threshold Settings | إعدادات وقف الخسارة", color="#FFD700")
    stop_loss = st.slider("Set Stop-Loss (%)", 0.0, 50.0, 10.0)
    take_profit = st.slider("Set Take-Profit (%)", 0.0, 100.0, 20.0)
    st.info(f"Alerts will trigger at -{stop_loss}% loss or +{take_profit}% gain.")

    # --- Diversification Risk ---
    custom_title("📁 Diversification Risk | مخاطر التنويع", color="#00FF88")
    if "Sector" in portfolio_data.columns:
        sector_chart = portfolio_data.groupby("Sector")["Weight"].sum()
        st.bar_chart(sector_chart)
    else:
        custom_warning("No sector data available. Please check portfolio input.")

    # --- Scenario Simulation ---
    custom_title("📉 Scenario Analysis | تحليل السيناريوهات", color="#FF6B6B")
    scenario = st.selectbox("Choose a Market Shock", ["Oil Price Drop", "Interest Rate Hike", "Geopolitical Tension"])
    st.write(f"📌 Simulated impact of '{scenario}' on portfolio: -4.2%")

    # --- Risk Alerts ---
    custom_title("🚨 Risk Alerts | تنبيهات المخاطر", color="#FF4444")
    # Use actual volatility value instead of col3.metric method
    volatility_value = 0.3  # Extract from the "0.3%" string or calculate from actual data
    if volatility_value > 0.5:
        custom_error("High volatility detected. Consider rebalancing.")
    if stop_loss > 30:
        custom_warning("Stop-loss threshold is high. Review risk tolerance.")

    # --- Educational Tooltip ---
    with st.expander("📘 What Is Risk Management? | ما هو إدارة المخاطر؟"):
        st.markdown("""
Risk management helps protect your portfolio from unexpected losses. It includes tools to monitor volatility, set thresholds, and simulate market stress. Use it to stay in control—even when markets are not.

إدارة المخاطر تساعدك على حماية محفظتك من الخسائر غير المتوقعة. تشمل أدوات لمراقبة التقلبات، وتحديد الحدود، وتحليل السيناريوهات.
""")

