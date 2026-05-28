from django.db import models
from apps.students.models import Student


class Note(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='study_material_notes')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_important = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.student.full_name}"


class QuestionPaper(models.Model):
    EXAM_TYPES = [
        ('board', 'Board Exam'), ('unit_test', 'Unit Test'),
        ('midterm', 'Mid-Term'), ('model', 'Model Paper'),
    ]
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    standard = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPES)
    year = models.IntegerField()
    file = models.FileField(upload_to='question_papers/')
    solution_file = models.FileField(upload_to='question_papers/solutions/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    download_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.subject} - {self.year} ({self.exam_type})"
