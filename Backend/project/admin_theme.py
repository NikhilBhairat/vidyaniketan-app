"""
Django Admin Theme Customization
Provides modern color schemes and styling for the admin interface
"""

# Color Theme Configuration
ADMIN_THEME_CONFIG = {
    'default': {
        'name': 'Vidyaniketan Purple',
        'primary_color': '#1A237E',      # Deep Purple
        'primary_light': '#3F51B5',      # Light Purple
        'primary_dark': '#0D1B4F',       # Very Dark Purple
        'accent_color': '#FF6F00',       # Deep Orange
        'accent_light': '#FFB74D',       # Light Orange
        'success_color': '#4CAF50',      # Green
        'warning_color': '#FFC107',      # Amber
        'danger_color': '#F44336',       # Red
        'info_color': '#2196F3',         # Blue
        'text_primary': '#212121',       # Dark Gray
        'text_secondary': '#757575',     # Gray
        'bg_primary': '#FFFFFF',         # White
        'bg_secondary': '#F5F5F5',       # Light Gray
        'border_color': '#E0E0E0',       # Border Gray
    },
    'modern_blue': {
        'name': 'Modern Blue',
        'primary_color': '#1976D2',      # Blue
        'primary_light': '#42A5F5',      # Light Blue
        'primary_dark': '#1565C0',       # Dark Blue
        'accent_color': '#FF6D00',       # Orange
        'accent_light': '#FFA040',       # Light Orange
        'success_color': '#388E3C',      # Dark Green
        'warning_color': '#FBC02D',      # Yellow
        'danger_color': '#D32F2F',       # Dark Red
        'info_color': '#0288D1',         # Cyan
        'text_primary': '#212121',
        'text_secondary': '#757575',
        'bg_primary': '#FFFFFF',
        'bg_secondary': '#FAFAFA',
        'border_color': '#BDBDBD',
    },
    'fresh_green': {
        'name': 'Fresh Green',
        'primary_color': '#00796B',      # Teal
        'primary_light': '#4DB6AC',      # Light Teal
        'primary_dark': '#004D40',       # Dark Teal
        'accent_color': '#D84315',       # Deep Orange
        'accent_light': '#FF6E40',       # Light Orange
        'success_color': '#2E7D32',      # Green
        'warning_color': '#F57F17',      # Amber
        'danger_color': '#C62828',       # Dark Red
        'info_color': '#0097A7',         # Cyan
        'text_primary': '#212121',
        'text_secondary': '#616161',
        'bg_primary': '#FFFFFF',
        'bg_secondary': '#F1F8E9',
        'border_color': '#B2DFDB',
    },
    'professional_slate': {
        'name': 'Professional Slate',
        'primary_color': '#455A64',      # Blue Grey
        'primary_light': '#78909C',      # Light Blue Grey
        'primary_dark': '#263238',       # Dark Blue Grey
        'accent_color': '#E65100',       # Orange
        'accent_light': '#FF7043',       # Light Orange
        'success_color': '#1B5E20',      # Dark Green
        'warning_color': '#FF8F00',      # Orange
        'danger_color': '#B71C1C',       # Dark Red
        'info_color': '#01579B',         # Dark Blue
        'text_primary': '#212121',
        'text_secondary': '#424242',
        'bg_primary': '#FFFFFF',
        'bg_secondary': '#ECEFF1',
        'border_color': '#90A4AE',
    },
}


def get_admin_css(theme_name='default'):
    """
    Generate CSS for Django admin with selected theme
    """
    config = ADMIN_THEME_CONFIG.get(theme_name, ADMIN_THEME_CONFIG['default'])
    
    css = f"""
    :root {{
        --admin-primary: {config['primary_color']};
        --admin-primary-light: {config['primary_light']};
        --admin-primary-dark: {config['primary_dark']};
        --admin-accent: {config['accent_color']};
        --admin-accent-light: {config['accent_light']};
        --admin-success: {config['success_color']};
        --admin-warning: {config['warning_color']};
        --admin-danger: {config['danger_color']};
        --admin-info: {config['info_color']};
        --admin-text-primary: {config['text_primary']};
        --admin-text-secondary: {config['text_secondary']};
        --admin-bg-primary: {config['bg_primary']};
        --admin-bg-secondary: {config['bg_secondary']};
        --admin-border: {config['border_color']};
    }}

    /* Header Styling */
    #header {{
        background-color: var(--admin-primary) !important;
        background: linear-gradient(135deg, var(--admin-primary) 0%, var(--admin-primary-dark) 100%) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        padding: 15px 20px;
    }}

    #header h1, #header h1 a, #header h1 a:visited {{
        color: white !important;
        font-weight: 600;
        font-size: 18px;
    }}

    #header h1 a:hover {{
        color: var(--admin-accent-light) !important;
    }}

    /* Navigation Styling */
    nav {{
        background-color: var(--admin-primary-dark) !important;
    }}

    .navbar {{
        background: linear-gradient(135deg, var(--admin-primary) 0%, var(--admin-primary-dark) 100%);
    }}

    /* Sidebar */
    #sidebar {{
        background-color: var(--admin-bg-secondary);
        border-right: 2px solid var(--admin-primary);
    }}

    .sidebar-nav, .sidebar-list {{
        background-color: var(--admin-bg-secondary);
    }}

    .sidebar-nav li a {{
        color: var(--admin-text-primary);
        border-left: 3px solid transparent;
        transition: all 0.3s ease;
    }}

    .sidebar-nav li a:hover {{
        background-color: var(--admin-accent);
        color: white;
        border-left-color: var(--admin-accent);
    }}

    .sidebar-nav li.active a {{
        background-color: var(--admin-primary);
        color: white;
        border-left-color: var(--admin-accent);
    }}

    /* Button Styling */
    .button, input[type="submit"], a.button {{
        background-color: var(--admin-primary) !important;
        background: linear-gradient(135deg, var(--admin-primary) 0%, var(--admin-primary-dark) 100%) !important;
        color: white !important;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
    }}

    .button:hover, input[type="submit"]:hover, a.button:hover {{
        background-color: var(--admin-primary-dark) !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }}

    .button:active, input[type="submit"]:active, a.button:active {{
        transform: translateY(1px);
    }}

    /* Success Button */
    .button.success, a.button.success {{
        background-color: var(--admin-success) !important;
    }}

    .button.success:hover, a.button.success:hover {{
        background-color: darkgreen !important;
    }}

    /* Danger Button */
    .button.danger, a.button.danger {{
        background-color: var(--admin-danger) !important;
    }}

    .button.danger:hover, a.button.danger:hover {{
        background-color: darkred !important;
    }}

    /* Links */
    a {{
        color: var(--admin-primary);
        text-decoration: none;
    }}

    a:visited {{
        color: var(--admin-primary-dark);
    }}

    a:hover {{
        color: var(--admin-accent);
        text-decoration: underline;
    }}

    /* Forms */
    fieldset {{
        border: 1px solid var(--admin-border);
        border-radius: 4px;
        background-color: var(--admin-bg-primary);
    }}

    fieldset h2 {{
        color: var(--admin-primary);
        border-bottom: 2px solid var(--admin-primary);
        padding-bottom: 10px;
        margin-bottom: 15px;
    }}

    input[type="text"], input[type="email"], input[type="password"], 
    input[type="number"], textarea, select {{
        border: 1px solid var(--admin-border);
        border-radius: 4px;
        padding: 8px 12px;
        font-size: 13px;
        transition: border-color 0.3s ease;
    }}

    input[type="text"]:focus, input[type="email"]:focus, input[type="password"]:focus,
    input[type="number"]:focus, textarea:focus, select:focus {{
        border-color: var(--admin-primary) !important;
        outline: none;
        box-shadow: 0 0 5px rgba(26, 35, 126, 0.2);
    }}

    /* Table Styling */
    table {{
        border-collapse: collapse;
        background-color: var(--admin-bg-primary);
    }}

    table thead th {{
        background-color: var(--admin-primary);
        color: white;
        padding: 12px 15px;
        text-align: left;
        font-weight: 600;
        border: none;
    }}

    table tbody tr {{
        border-bottom: 1px solid var(--admin-border);
        transition: background-color 0.2s ease;
    }}

    table tbody tr:hover {{
        background-color: var(--admin-bg-secondary);
    }}

    table tbody tr:nth-child(even) {{
        background-color: rgba(0, 0, 0, 0.01);
    }}

    table td {{
        padding: 12px 15px;
        border: none;
    }}

    /* Messages */
    .messagelist {{
        margin: 10px 0;
    }}

    .messagelist li {{
        padding: 12px 15px;
        border-radius: 4px;
        margin-bottom: 5px;
        border-left: 4px solid;
    }}

    .messagelist .success {{
        background-color: #E8F5E9;
        border-left-color: var(--admin-success);
        color: #1B5E20;
    }}

    .messagelist .error {{
        background-color: #FFEBEE;
        border-left-color: var(--admin-danger);
        color: #B71C1C;
    }}

    .messagelist .warning {{
        background-color: #FFF3E0;
        border-left-color: var(--admin-warning);
        color: #E65100;
    }}

    .messagelist .info {{
        background-color: #E3F2FD;
        border-left-color: var(--admin-info);
        color: #01579B;
    }}

    /* Search Box */
    #searchbar {{
        background-color: var(--admin-bg-secondary);
        border: 1px solid var(--admin-border);
        border-radius: 4px;
        padding: 10px 15px;
    }}

    #searchbar input {{
        border: none;
        background-color: transparent;
        color: var(--admin-text-primary);
    }}

    #searchbar input::placeholder {{
        color: var(--admin-text-secondary);
    }}

    /* Pagination */
    .pagination {{
        display: flex;
        gap: 5px;
        margin: 20px 0;
    }}

    .pagination a, .pagination span {{
        padding: 8px 12px;
        border: 1px solid var(--admin-border);
        border-radius: 4px;
        color: var(--admin-primary);
        background-color: var(--admin-bg-primary);
        text-decoration: none;
        transition: all 0.3s ease;
    }}

    .pagination a:hover {{
        background-color: var(--admin-primary);
        color: white;
    }}

    .pagination .this-page {{
        background-color: var(--admin-primary);
        color: white;
        border-color: var(--admin-primary);
    }}

    /* Breadcrumbs */
    .breadcrumbs {{
        background-color: var(--admin-bg-secondary);
        padding: 10px 15px;
        border-radius: 4px;
        margin-bottom: 15px;
    }}

    .breadcrumbs a {{
        color: var(--admin-primary);
    }}

    /* Module Listing */
    .module {{
        border: 1px solid var(--admin-border);
        border-radius: 4px;
        background-color: var(--admin-bg-primary);
        margin-bottom: 15px;
        overflow: hidden;
    }}

    .module h2 {{
        background-color: var(--admin-primary);
        color: white;
        padding: 12px 15px;
        margin: 0;
        font-size: 16px;
        border-bottom: none;
    }}

    .module table {{
        width: 100%;
    }}

    /* Action Checkbox */
    .actions {{
        background-color: var(--admin-bg-secondary);
        padding: 12px 15px;
        border-bottom: 1px solid var(--admin-border);
        border-radius: 4px 4px 0 0;
    }}

    .actions select {{
        border-color: var(--admin-border);
    }}

    /* Inline Styles */
    .inline-group {{
        border: 1px solid var(--admin-border);
        border-radius: 4px;
        margin-bottom: 10px;
    }}

    .inline-group .module {{
        border: none;
        margin-bottom: 0;
    }}

    /* Help Text */
    p.help, .help-text {{
        color: var(--admin-text-secondary);
        font-size: 12px;
        margin-top: 5px;
    }}

    /* Errors */
    .errorlist {{
        color: var(--admin-danger);
        padding: 10px;
        background-color: #FFEBEE;
        border: 1px solid var(--admin-danger);
        border-radius: 4px;
        margin-bottom: 10px;
    }}

    .errorlist li {{
        margin: 5px 0;
    }}

    /* Responsive */
    @media (max-width: 600px) {{
        #header {{
            padding: 10px;
        }}

        .button, input[type="submit"], a.button {{
            padding: 6px 12px;
            font-size: 12px;
        }}

        table {{
            font-size: 12px;
        }}

        table td, table th {{
            padding: 8px 10px;
        }}
    }}
    """
    
    return css


def get_admin_base_template(theme_name='default'):
    """
    Generate base admin template HTML with theme styling
    """
    config = ADMIN_THEME_CONFIG.get(theme_name, ADMIN_THEME_CONFIG['default'])
    
    html = f"""
    {{% extends "admin/base.html" %}}
    {{% load static %}}

    {{% block extrahead %}}
    <style>
    {get_admin_css(theme_name)}
    </style>
    <style>
    /* Custom branding */
    #branding h1 {{
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 24px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }}

    /* Admin site name */
    #site-name {{
        color: white;
        font-weight: 700;
        font-size: 18px;
    }}

    /* Logo area */
    .logo-area {{
        display: flex;
        align-items: center;
        gap: 15px;
    }}

    .logo-area img {{
        height: 40px;
        width: auto;
    }}
    </style>
    {{% endblock %}}
    """
    
    return html
