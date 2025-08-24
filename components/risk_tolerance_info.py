import streamlit as st

def show_risk_info():
    with st.expander("🛡️ What Does Risk Tolerance Mean?"):
        st.markdown("""
**Risk tolerance** reflects how comfortable you are with potential losses in pursuit of higher returns. It helps the AI tailor stock recommendations to match your financial personality.

---

### 🎯 Why It Matters
- A **high risk tolerance** means you're willing to accept short-term volatility for long-term gains.
- A **low risk tolerance** means you prefer stability, even if it means lower returns.

---

### 📊 How to Use the Slider

| Risk Level | Description | AI Behavior |
|------------|-------------|-------------|
| **0–30**   | Conservative | Focuses on stable, dividend-paying stocks (e.g., banks, utilities) |
| **31–70**  | Moderate     | Mix of growth and defensive stocks, balanced across sectors |
| **71–100** | Aggressive   | Prioritizes high-growth, volatile stocks (e.g., tech, speculative plays) |

---

### 🧪 Example Scenarios
- **Ahmed**, age 55, nearing retirement → Sets risk tolerance to **25**  
  → AI recommends low-volatility stocks with strong fundamentals

- **Sara**, age 30, long-term investor → Sets risk tolerance to **75**  
  → AI suggests emerging sector picks with higher upside potential

---

### 🧠 Tips for Beginners
- Start with **30–50** if you're unsure — this gives a balanced portfolio.
- Adjust gradually as you learn more about market behavior.
- Use the **AI Forecast Confidence** alongside risk level to make smarter decisions.

---

### 📌 Note for Committee Users
Risk tolerance can also be used to simulate different investor profiles for oversight and benchmarking. It's a powerful tool for understanding how recommendations shift across risk bands.
""")
