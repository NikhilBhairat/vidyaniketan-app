from django.db import models


class GalleryCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class GalleryItem(models.Model):
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE,
                                  related_name='items', null=True, blank=True)
    file = models.FileField(upload_to='gallery/', blank=True, null=True)
    video_url = models.CharField(max_length=500, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        category_name = self.category.name if self.category else "No Category"
        return f"{category_name} - {self.uploaded_at}"
