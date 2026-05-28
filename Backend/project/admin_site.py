"""
Custom Django Admin Site Configuration with Theme Support
"""
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group
from django.utils.html import format_html
from project.admin_theme import ADMIN_THEME_CONFIG, get_admin_css


class VidyanikketanAdminSite(AdminSite):
    """
    Custom admin site with theme customization for Vidyaniketan
    """
    
    # Site configuration
    site_header = "Vidyaniketan Classes & Academy"
    site_title = "Admin Panel"
    index_title = "Welcome to Administration Dashboard"
    
    # Theme selection - can be changed to: 'default', 'modern_blue', 'fresh_green', 'professional_slate'
    current_theme = 'default'
    
    def get_theme_config(self):
        """Get current theme configuration"""
        return ADMIN_THEME_CONFIG.get(self.current_theme, ADMIN_THEME_CONFIG['default'])
    
    def get_theme_name(self):
        """Get current theme display name"""
        config = self.get_theme_config()
        return config.get('name', 'Vidyaniketan Purple')
    
    def extra_head(self, request):
        """Add custom CSS to admin head"""
        css = get_admin_css(self.current_theme)
        return format_html(
            '<style>\n{}\n</style>\n'
            '<meta name="theme-color" content="{}">\n',
            css,
            self.get_theme_config()['primary_color']
        )
    
    def each_context(self, request):
        """Add theme context to all admin pages"""
        context = super().each_context(request)
        context.update({
            'theme_name': self.get_theme_name(),
            'theme_config': self.get_theme_config(),
            'available_themes': [
                {'key': k, 'name': v['name']} 
                for k, v in ADMIN_THEME_CONFIG.items()
            ]
        })
        return context
    
    def index(self, request, extra_context=None):
        """Override index to add custom context"""
        extra_context = extra_context or {}
        extra_context.update({
            'theme_info': {
                'current': self.get_theme_name(),
                'available': list(ADMIN_THEME_CONFIG.keys())
            }
        })
        return super().index(request, extra_context)


# Create custom admin site instance
vidyaniketan_admin_site = VidyanikketanAdminSite(name='vidyaniketan_admin')
