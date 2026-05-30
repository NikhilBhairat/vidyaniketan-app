from django.db import models
from apps.accounts.models import User
from apps.students.models import Student


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('general', 'General'), ('fees', 'Fees'), ('marks', 'Marks'),
        ('attendance', 'Attendance'), ('timetable', 'Timetable'),
        ('event', 'Event'), ('holiday', 'Holiday'),
    ]
    AUDIENCE_CHOICES = [
        ('all', 'All'), ('standard', 'Specific Standard'), ('student', 'Specific Student'),
    ]
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=15, choices=NOTIFICATION_TYPES, default='general')
    audience = models.CharField(max_length=10, choices=AUDIENCE_CHOICES, default='all')
    target_standard = models.CharField(max_length=100, null=True, blank=True)
    target_students = models.ManyToManyField(Student, blank=True, related_name='notifications')
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.notification_type})"


class NotificationRead(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE,
                                      related_name='read_by')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    read_at = models.DateTimeField(null=True, blank=True)  # ✅ FIXED: Removed auto_now_add
    created_at = models.DateTimeField(auto_now_add=True)    # ✅ NEW: Track record creation time

    class Meta:
        unique_together = ('notification', 'user')

    def __str__(self):
        return f"{self.notification.title} - {self.user.mobile_number}"
