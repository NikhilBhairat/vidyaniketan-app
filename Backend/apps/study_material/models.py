from django.db import models
from django.core.validators import FileExtensionValidator
from apps.students.models import Student


class Note(models.Model):
    STANDARD_CHOICES = [
        ('5', '5th Standard'),
        ('6', '6th Standard'),
        ('7', '7th Standard'),
        ('8', '8th Standard'),
        ('9', '9th Standard'),
        ('10', '10th Standard'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='study_material_notes',
        null=True,
        blank=True,
        help_text='Deprecated: notes are served standard-wise in the student app.'
    )
    standard = models.CharField(max_length=10, choices=STANDARD_CHOICES, db_index=True)
    subject = models.CharField(max_length=100, blank=True, db_index=True)
    chapter = models.CharField(max_length=150, blank=True, db_index=True)
    title = models.CharField(max_length=255, blank=True, default='')
    content = models.TextField(blank=True, default='')
    pdf_file = models.FileField(
        upload_to='notes/pdfs/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_important = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Chapter-wise Note'
        verbose_name_plural = 'Chapter-wise Notes'

    def save(self, *args, **kwargs):
        if not self.title:
            fallback_title = self.chapter or self.subject or 'Chapter-wise Note'
            self.title = fallback_title
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.standard or 'General'}"


class QuestionPaper(models.Model):
    STANDARD_CHOICES = Note.STANDARD_CHOICES

    EXAM_TYPES = [
        ('board', 'Board Exam'), ('unit_test', 'Unit Test'),
        ('midterm', 'Mid-Term'), ('model', 'Model Paper'),
    ]
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    standard = models.CharField(max_length=10, choices=STANDARD_CHOICES, db_index=True)
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPES)
    year = models.IntegerField()
    file = models.FileField(upload_to='question_papers/')
    solution_file = models.FileField(upload_to='question_papers/solutions/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    download_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.subject} - {self.year} ({self.exam_type})"
