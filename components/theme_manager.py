"""
Theme Manager for TADAWUL NEXUS
Provides scalable theming system for multi-user SaaS platform
"""

class ThemeManager:
    """Manages themes and user preferences for the application"""
    
    # Default themes
    THEMES = {
        'dark_professional': {
            'name': 'Dark Professional',
            'primary_bg': '#0E1117',
            'secondary_bg': '#1E2A3A',
            'sidebar_bg': '#1E2A3A',
            'sidebar_text': '#FFFFFF',
            'main_text': '#FFFFFF',
            'accent_color': '#00D4FF',
            'success_color': '#00CC88',
            'warning_color': '#FFB800',
            'error_color': '#FF6B6B',
            'border_color': 'rgba(255, 255, 255, 0.1)',
            'glass_bg': 'rgba(30, 42, 58, 0.8)',
        },
        'light_minimal': {
            'name': 'Light Minimal',
            'primary_bg': '#FFFFFF',
            'secondary_bg': '#F8F9FA',
            'sidebar_bg': '#F8F9FA',
            'sidebar_text': '#2C3E50',
            'main_text': '#2C3E50',
            'accent_color': '#007BFF',
            'success_color': '#28A745',
            'warning_color': '#FFC107',
            'error_color': '#DC3545',
            'border_color': 'rgba(0, 0, 0, 0.1)',
            'glass_bg': 'rgba(248, 249, 250, 0.9)',
        },
        'saudi_green': {
            'name': 'Saudi Green',
            'primary_bg': '#0F1419',
            'secondary_bg': '#1B5E20',
            'sidebar_bg': '#1B5E20',
            'sidebar_text': '#FFFFFF',
            'main_text': '#FFFFFF',
            'accent_color': '#4CAF50',
            'success_color': '#66BB6A',
            'warning_color': '#FFB74D',
            'error_color': '#EF5350',
            'border_color': 'rgba(76, 175, 80, 0.3)',
            'glass_bg': 'rgba(27, 94, 32, 0.8)',
        },
        'high_contrast': {
            'name': 'High Contrast (Accessibility)',
            'primary_bg': '#000000',
            'secondary_bg': '#1A1A1A',
            'sidebar_bg': '#1A1A1A',
            'sidebar_text': '#FFFFFF',
            'main_text': '#FFFFFF',
            'accent_color': '#FFFF00',
            'success_color': '#00FF00',
            'warning_color': '#FFFF00',
            'error_color': '#FF0000',
            'border_color': '#FFFFFF',
            'glass_bg': 'rgba(26, 26, 26, 0.95)',
        }
    }
    
    @staticmethod
    def get_theme_css(theme_name='dark_professional', user_overrides=None):
        """Generate CSS for the specified theme with optional user overrides"""
        
        if theme_name not in ThemeManager.THEMES:
            theme_name = 'dark_professional'
        
        theme = ThemeManager.THEMES[theme_name].copy()
        
        # Apply user overrides if provided
        if user_overrides:
            theme.update(user_overrides)
        
        return f"""
        <style>
        /* ========================================
           THEME: {theme['name']}
           Scalable CSS Variables Approach
           ======================================== */
        
        :root {{
            --primary-bg: {theme['primary_bg']};
            --secondary-bg: {theme['secondary_bg']};
            --sidebar-bg: {theme['sidebar_bg']};
            --sidebar-text: {theme['sidebar_text']};
            --main-text: {theme['main_text']};
            --accent-color: {theme['accent_color']};
            --success-color: {theme['success_color']};
            --warning-color: {theme['warning_color']};
            --error-color: {theme['error_color']};
            --border-color: {theme['border_color']};
            --glass-bg: {theme['glass_bg']};
        }}
        
        /* CLEAN SIDEBAR STYLING - NO !important NEEDED */
        div[data-testid="stSidebar"] {{
            background-color: var(--sidebar-bg);
            color: var(--sidebar-text);
        }}
        
        div[data-testid="stSidebar"] * {{
            color: var(--sidebar-text);
        }}
        
        /* Specific element targeting without aggression */
        div[data-testid="stSidebar"] .stMarkdown h1,
        div[data-testid="stSidebar"] .stMarkdown h2,
        div[data-testid="stSidebar"] .stMarkdown h3,
        div[data-testid="stSidebar"] .stMarkdown h4,
        div[data-testid="stSidebar"] .stMarkdown h5,
        div[data-testid="stSidebar"] .stMarkdown h6 {{
            color: var(--sidebar-text);
            font-weight: 600;
        }}
        
        /* Metric containers */
        div[data-testid="stSidebar"] div[data-testid="metric-container"] * {{
            color: var(--sidebar-text);
        }}
        
        /* Main app styling */
        .stApp {{
            background-color: var(--primary-bg);
            color: var(--main-text);
        }}
        
        /* Cards and containers */
        .portfolio-card {{
            background: var(--glass-bg);
            border: 1px solid var(--border-color);
            color: var(--main-text);
        }}
        
        /* Success/Warning/Error colors */
        .success-text {{
            color: var(--success-color);
        }}
        
        .warning-text {{
            color: var(--warning-color);
        }}
        
        .error-text {{
            color: var(--error-color);
        }}
        
        /* Accent elements */
        .accent-border {{
            border-color: var(--accent-color);
        }}
        
        .accent-text {{
            color: var(--accent-color);
        }}
        </style>
        """
    
    @staticmethod
    def get_user_theme_selector():
        """Returns HTML for theme selection dropdown"""
        return """
        <div class="theme-selector">
            <label for="theme-select">Choose Theme:</label>
            <select id="theme-select" onchange="changeTheme(this.value)">
                <option value="dark_professional">Dark Professional</option>
                <option value="light_minimal">Light Minimal</option>
                <option value="saudi_green">Saudi Green</option>
                <option value="high_contrast">High Contrast</option>
            </select>
        </div>
        """
    
    @staticmethod
    def save_user_theme_preference(user_id, theme_name, custom_overrides=None):
        """Save user's theme preference to database (placeholder)"""
        # In a real SaaS app, this would save to your user database
        import json
        
        user_prefs = {
            'theme': theme_name,
            'custom_overrides': custom_overrides or {}
        }
        
        # For now, save to a local file (replace with database in production)
        try:
            with open(f'user_themes/{user_id}_theme.json', 'w') as f:
                json.dump(user_prefs, f)
            return True
        except:
            return False
    
    @staticmethod
    def load_user_theme_preference(user_id):
        """Load user's theme preference from database (placeholder)"""
        import json
        
        try:
            with open(f'user_themes/{user_id}_theme.json', 'r') as f:
                return json.load(f)
        except:
            return {'theme': 'dark_professional', 'custom_overrides': {}}
