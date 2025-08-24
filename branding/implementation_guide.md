# TADAWUL NEXUS Branding Implementation Guide

## 🚀 Quick Start

### 1. File Structure
```
Saudi Stock Market App/
├── branding/
│   ├── logos/
│   │   ├── tadawul_nexus_logo.svg (Light mode)
│   │   ├── tadawul_nexus_logo_dark.svg (Dark mode)
│   │   └── tadawul_nexus_bilingual.svg (Arabic-English)
│   ├── assets/
│   ├── tadawul_branding.py (Main branding module)
│   └── brand_guidelines.md (Complete guidelines)
├── apps/
│   └── enhanced_saudi_app_v2.py (Updated with branding)
└── branding_demo.py (Demo application)
```

### 2. Basic Implementation

```python
# Import the branding system
from branding.tadawul_branding import TadawulBranding

# Apply branding to your Streamlit app
def main():
    # Apply complete branding system
    TadawulBranding.apply_branding()
    
    # Display professional header with logo
    TadawulBranding.display_header(
        title="TADAWUL NEXUS",
        tagline="primary",
        include_logo=True
    )
    
    # Your app content here...
    
    # Display professional footer
    TadawulBranding.display_footer()
```

## 🎨 Branding Components

### Logo Usage
```python
# Display different logo variants
TadawulBranding.display_logo("light", width=180)    # Light backgrounds
TadawulBranding.display_logo("dark", width=180)     # Dark backgrounds  
TadawulBranding.display_logo("bilingual", width=220) # Official documents
```

### Professional Headers
```python
# Different header styles
TadawulBranding.display_header("TADAWUL NEXUS", "primary")
TadawulBranding.display_header("Portfolio Manager", "gateway") 
TadawulBranding.display_header("Analytics Dashboard", "technical")
```

### Styled Metrics
```python
# Success/warning styled metrics
TadawulBranding.success_metric("Portfolio Return", "8.5%", "+1.2%")
TadawulBranding.warning_metric("Volatility", "12.3%", "+0.8%")
```

## 📊 Chart Styling

### Plotly Integration
```python
import plotly.graph_objects as go

# Use brand colors in charts
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=dates, y=prices,
    name="Portfolio",
    line=dict(color=TadawulBranding.COLORS['primary_blue'], width=3)
))

# Market comparison
fig.add_trace(go.Scatter(
    x=dates, y=market_prices,
    name="TASI",
    line=dict(color=TadawulBranding.COLORS['accent_orange'], width=2)
))
```

### Bar Charts
```python
import plotly.express as px

# Sector allocation with brand colors
fig = px.bar(
    df, x='percentage', y='sector',
    orientation='h',
    title="Portfolio Allocation",
    color='percentage',
    color_continuous_scale='Blues'
)
```

## 🌍 Bilingual Support

### Arabic Text
```python
# Proper Arabic text rendering
st.markdown("""
<div class="arabic-text">
تداول نكسس - منصة ذكية للأسواق السعودية
</div>
""", unsafe_allow_html=True)
```

### Tagline Selection
```python
# Use appropriate taglines
english_tagline = TadawulBranding.TAGLINES['primary']
arabic_tagline = TadawulBranding.TAGLINES['arabic']
```

## 📱 Responsive Design

### Streamlit Configuration
```python
st.set_page_config(
    page_title="TADAWUL NEXUS",
    page_icon="📊", 
    layout="wide",
    initial_sidebar_state="expanded"
)
```

### Adaptive Layouts
```python
# Responsive columns
col1, col2, col3 = st.columns([1, 2, 1])  # Automatically adapts

# Mobile-friendly metrics
if st.sidebar.checkbox("Mobile View"):
    # Single column layout
    for metric in metrics:
        st.metric(metric['label'], metric['value'])
else:
    # Multi-column layout
    cols = st.columns(len(metrics))
    for i, metric in enumerate(metrics):
        with cols[i]:
            st.metric(metric['label'], metric['value'])
```

## 🎯 Usage Guidelines

### Committee Memos
```python
# For official VB committee documents
TadawulBranding.display_logo("bilingual", width=200)
st.markdown("## Investment Committee Analysis")
st.markdown(f"*{TadawulBranding.TAGLINES['primary']}*")
```

### Dashboard Headers
```python
# For main application pages
TadawulBranding.display_header("Portfolio Dashboard", "gateway")
```

### Report Generation
```python
# For exported reports
def generate_report():
    TadawulBranding.apply_branding()
    TadawulBranding.display_logo("light", width=150)
    # Report content...
    TadawulBranding.display_footer()
```

## 🔧 Customization

### Custom Colors
```python
# Extend brand colors
custom_colors = TadawulBranding.COLORS.copy()
custom_colors['custom_purple'] = '#6B46C1'

# Use in charts
fig.update_traces(marker_color=custom_colors['custom_purple'])
```

### Custom Taglines
```python
# Add project-specific taglines
custom_taglines = TadawulBranding.TAGLINES.copy()
custom_taglines['committee'] = "Supporting VB Investment Decisions"
```

## 📋 Quality Checklist

### Before Deployment
- [ ] Logo displays correctly in all sizes
- [ ] Colors match brand guidelines
- [ ] Arabic text renders properly (if used)
- [ ] Charts use consistent color scheme
- [ ] Responsive design works on mobile
- [ ] Footer appears on all pages
- [ ] Loading performance is acceptable

### VB Compliance
- [ ] Uses official VB color palette
- [ ] Maintains professional tone
- [ ] Supports governance requirements
- [ ] Includes proper attribution
- [ ] Meets accessibility standards

## 🚀 Advanced Features

### Dynamic Theming
```python
# Theme switching based on user preference
theme = st.sidebar.selectbox("Theme", ["Light", "Dark"])
logo_type = "light" if theme == "Light" else "dark"
TadawulBranding.display_logo(logo_type)
```

### Print Optimization
```python
# Print-friendly styling
st.markdown("""
<style>
@media print {
    .logo-container { 
        background: white !important; 
        box-shadow: none !important;
    }
}
</style>
""", unsafe_allow_html=True)
```

### Performance Optimization
```python
# Cache branding resources
@st.cache_resource
def load_branding():
    return TadawulBranding()

branding = load_branding()
branding.apply_branding()
```

## 📞 Support

For branding implementation support:
1. Review `brand_guidelines.md` for detailed specifications
2. Check `branding_demo.py` for working examples
3. Test responsive design across devices
4. Validate Arabic text rendering (if applicable)

**Remember**: Consistency is key for professional branding. Use the same logo, colors, and styling across all components of your application.
