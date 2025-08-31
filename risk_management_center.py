import streamlit as st
import pandas as pd

def risk_management_center(portfolio_data, market_data):
    st.sidebar.markdown("🛡️ **Risk Management Center**")

    st.title("🛡️ Risk Management Center")
    st.caption("تحليل المخاطر المالية للمحفظة | Portfolio Risk Analysis")

    # --- Metrics Section ---
    st.subheader("📊 Key Risk Metrics | مؤشرات المخاطر")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📉 Max Drawdown", "-26.1%", "أقصى انخفاض")
    col2.metric("📈 Portfolio Beta", "1.00", "بيتا المحفظة")
    col3.metric("📊 Volatility", "0.3%", "التقلب")
    col4.metric("⚖️ Sharpe Ratio", "-0.54", "نسبة شارب")

    # --- Stop-Loss & Take-Profit ---
    st.subheader("🎯 Threshold Settings | إعدادات وقف الخسارة")
    stop_loss = st.slider("Set Stop-Loss (%)", 0.0, 50.0, 10.0)
    take_profit = st.slider("Set Take-Profit (%)", 0.0, 100.0, 20.0)
    st.info(f"Alerts will trigger at -{stop_loss}% loss or +{take_profit}% gain.")

    # --- Diversification Risk ---
    st.subheader("📁 Diversification Risk | مخاطر التنويع")
    if "Sector" in portfolio_data.columns:
        sector_chart = portfolio_data.groupby("Sector")["Weight"].sum()
        st.bar_chart(sector_chart)
    else:
        st.warning("No sector data available. Please check portfolio input.")

    # --- Scenario Simulation ---
    st.subheader("📉 Scenario Analysis | تحليل السيناريوهات")
    scenario = st.selectbox("Choose a Market Shock", ["Oil Price Drop", "Interest Rate Hike", "Geopolitical Tension"])
    st.write(f"📌 Simulated impact of '{scenario}' on portfolio: -4.2%")

    # --- Risk Alerts ---
    st.subheader("🚨 Risk Alerts | تنبيهات المخاطر")
    if float(col3.metric) > 0.5:
        st.error("⚠️ High volatility detected. Consider rebalancing.")
    if stop_loss > 30:
        st.warning("⚠️ Stop-loss threshold is high. Review risk tolerance.")

    # --- Educational Tooltip ---
    with st.expander("📘 What Is Risk Management? | ما هو إدارة المخاطر؟"):
        st.markdown("""
Risk management helps protect your portfolio from unexpected losses. It includes tools to monitor volatility, set thresholds, and simulate market stress. Use it to stay in control—even when markets are not.

إدارة المخاطر تساعدك على حماية محفظتك من الخسائر غير المتوقعة. تشمل أدوات لمراقبة التقلبات، وتحديد الحدود، وتحليل السيناريوهات.
""")

