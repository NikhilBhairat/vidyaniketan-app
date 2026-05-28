from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import Student
from project.admin_site import vidyaniketan_admin_site


class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'student_id', 'full_name', 'roll_number', 'school_name', 'standard', 'gender_badge', 'status_badge', 'admission_date']
    search_fields = ['student_id', 'full_name', 'roll_number', 'school_name', 'standard']
    list_filter = ['is_active', 'standard', 'gender', 'school_name', 'admission_date']
    ordering = ['-admission_date']
    list_per_page = 20
    readonly_fields = ['student_id']

    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'student_id', 'full_name', 'roll_number', 'standard', 'school_name'),
            'classes': ('wide',),
        }),
        ('Personal Details', {
            'fields': ('date_of_birth', 'gender', 'blood_group', 'profile_photo', 'address'),
            'classes': ('wide',),
        }),
        ('Contact Information', {
            'fields': ('mobile_number',),
            'classes': ('wide',),
        }),
        ('Academic Status', {
            'fields': ('admission_date', 'receive_admin_alerts', 'is_active'),
            'classes': ('collapse',),
        }),
    )

    def gender_badge(self, obj):
        if obj.gender == 'Male':
            return format_html('<span class="badge badge-male">♂ Male</span>')
        elif obj.gender == 'Female':
            return format_html('<span class="badge badge-female">♀ Female</span>')
        return format_html('<span class="badge badge-other">Other</span>')
    gender_badge.short_description = 'Gender'
    gender_badge.admin_order_field = 'gender'

    def status_badge(self, obj):
        if obj.is_active:
            return format_html('<span class="badge badge-active">Active</span>')
        return format_html('<span class="badge badge-inactive">Inactive</span>')
    status_badge.short_description = 'Status'
    status_badge.admin_order_field = 'is_active'


# Register with custom admin site
vidyaniketan_admin_site.register(Student, StudentAdmin)