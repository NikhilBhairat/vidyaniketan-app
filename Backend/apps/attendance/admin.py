from django.contrib import admin
from .models import Attendance
from project.admin_site import vidyaniketan_admin_site

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'date', 'status']
    search_fields = ['student__full_name', 'student__student_id']
    list_filter = ['date', 'status']
    date_hierarchy = 'date'
    ordering = ['-date']
    list_per_page = 20

# Register with custom admin site
vidyaniketan_admin_site.register(Attendance, AttendanceAdmin)