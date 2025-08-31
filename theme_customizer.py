import streamlit as st

def theme_customizer():
    st.title("🎨 Theme Customizer")
    st.caption("تحكم في ألوان التطبيق | Customize Your App Colors")

    with st.expander("🛠️ Customize Theme Settings"):
        st.markdown("Choose your preferred colors and font style:")

        # --- Color Pickers ---
        bg_color = st.color_picker("Background Color", "#f5f7fa")
        heading_color = st.color_picker("Heading Text Color", "#0054A3")
        font_choice = st.selectbox("Font Style", ["sans-serif", "serif", "monospace"])

        # --- Preview Section ---
        st.markdown(f"""
        <style>
        body {{
            background-color: {bg_color};
            font-family: {font_choice};
        }}
        h1, h2, h3 {{
            color: {heading_color};
        }}
        </style>
        """, unsafe_allow_html=True)

        st.markdown(f"<h2 style='color:{heading_color};font-family:{font_choice};'>Live Preview</h2>", unsafe_allow_html=True)
        st.write("This is how your headings and background will appear.")

        st.success("✅ Theme settings applied. You can save these preferences for future sessions.")
