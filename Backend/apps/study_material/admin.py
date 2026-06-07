from django.contrib import admin
from django.utils.html import format_html
from .models import Note, QuestionPaper
from project.admin_site import vidyaniketan_admin_site


class NoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'standard', 'subject', 'chapter', 'has_pdf', 'importance_badge', 'created_at']
    search_fields = ['title', 'content', 'subject', 'chapter', 'standard']
    list_filter = ['is_important', 'standard', 'subject', 'created_at']
    ordering = ['-created_at']
    list_per_page = 20

    fieldsets = (
        ('Hierarchy', {
            'fields': ('standard', 'subject', 'chapter'),
            'classes': ('wide',),
        }),
        ('Chapter-wise Note Information', {
            'fields': ('pdf_file',),
            'classes': ('wide',),
        }),
        ('Settings', {
            'fields': ('is_important',),
            'classes': ('collapse',),
        }),
    )

    def importance_badge(self, obj):
        if obj.is_important:
            return format_html('<span class="badge badge-important">Important</span>')
        return format_html('<span class="badge badge-normal">Normal</span>')
    importance_badge.short_description = 'Importance'
    importance_badge.admin_order_field = 'is_important'

    def truncated_content(self, obj):
        if len(obj.content) > 50:
            return format_html('{}...', obj.content[:50])
        return obj.content
    truncated_content.short_description = 'Content'

    def has_pdf(self, obj):
        return bool(obj.pdf_file)
    has_pdf.boolean = True
    has_pdf.short_description = 'PDF'

class QuestionPaperAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'subject', 'standard', 'exam_type', 'year', 'uploaded_at']
    search_fields = ['title', 'subject', 'standard']
    list_filter = ['exam_type', 'standard', 'year']
    ordering = ['-uploaded_at']
    list_per_page = 20

# Register with custom admin site
vidyaniketan_admin_site.register(Note, NoteAdmin)
vidyaniketan_admin_site.register(QuestionPaper, QuestionPaperAdmin)
