from django.contrib import admin
from .models import Notification
from project.admin_site import vidyaniketan_admin_site


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'notification_type', 'audience', 'is_sent', 'created_at']
    search_fields = ['title', 'message']
    list_filter = ['notification_type', 'audience', 'is_sent', 'created_at']
    ordering = ['-created_at']
    list_per_page = 20


# Register with custom admin site
vidyaniketan_admin_site.register(Notification, NotificationAdmin)
