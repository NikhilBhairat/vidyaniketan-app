from django.db import models


class RecordedLecture(models.Model):
    PLATFORM_CHOICES = [
        ('youtube', 'YouTube'), ('vimeo', 'Vimeo'),
        ('drive', 'Google Drive'), ('upload', 'Direct Upload'),
    ]
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=100, blank=True, null=True)
    chapter = models.CharField(max_length=100, blank=True, null=True)
    teacher = models.CharField(max_length=100, blank=True, null=True)
    platform = models.CharField(max_length=10, choices=PLATFORM_CHOICES, default='youtube')
    video_url = models.URLField(blank=True)
    video_file = models.FileField(upload_to='lectures/videos/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='lectures/thumbnails/', blank=True, null=True)
    duration_minutes = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    view_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} - {self.subject}"
