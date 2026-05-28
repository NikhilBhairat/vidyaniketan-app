from django.db import models
from apps.students.models import Student


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Late'),
        ('H', 'Holiday'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    # subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    # marked_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    remarks = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.student} - {self.date} - {self.get_status_display()}"
