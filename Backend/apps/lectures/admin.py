from django.contrib import admin
from .models import RecordedLecture
from project.admin_site import vidyaniketan_admin_site


class RecordedLectureAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'subject', 'teacher', 'platform', 'duration_minutes', 'uploaded_at', 'is_active']
    search_fields = ['title', 'subject', 'teacher', 'description']
    list_filter = ['platform', 'is_active', 'uploaded_at']
    date_hierarchy = 'uploaded_at'
    ordering = ['-uploaded_at']
    list_per_page = 20


# Register with custom admin site
vidyaniketan_admin_site.register(RecordedLecture, RecordedLectureAdmin)
