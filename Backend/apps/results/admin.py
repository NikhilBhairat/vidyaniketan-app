from django.contrib import admin
from .models import Exam, Mark
from project.admin_site import vidyaniketan_admin_site


class ExamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'exam_type', 'standard', 'academic_year', 'start_date', 'end_date']
    search_fields = ['name', 'standard']
    list_filter = ['exam_type', 'standard', 'academic_year']
    date_hierarchy = 'start_date'
    ordering = ['-start_date']
    list_per_page = 20


class MarkAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'exam', 'subject', 'marks_obtained', 'grade', 'is_absent']
    search_fields = ['student__full_name', 'subject', 'exam__name']
    list_filter = ['exam', 'grade', 'is_absent']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    list_per_page = 20


# Register with custom admin site
vidyaniketan_admin_site.register(Exam, ExamAdmin)
vidyaniketan_admin_site.register(Mark, MarkAdmin)