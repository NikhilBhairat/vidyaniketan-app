from django.contrib import admin
from .models import GalleryCategory, GalleryItem
from project.admin_site import vidyaniketan_admin_site


class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name']
    ordering = ['name']
    list_per_page = 20


class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'file', 'video_url', 'uploaded_at']
    search_fields = ['category__name']
    list_filter = ['category', 'uploaded_at']
    date_hierarchy = 'uploaded_at'
    ordering = ['-uploaded_at']
    list_per_page = 20


# Register with custom admin site
vidyaniketan_admin_site.register(GalleryCategory, GalleryCategoryAdmin)
vidyaniketan_admin_site.register(GalleryItem, GalleryItemAdmin)
