from django.db import models
from apps.students.models import Student


class Exam(models.Model):
    EXAM_TYPES = [
        ('unit_test', 'Unit Test'),
        ('midterm', 'Mid-Term'),
        ('prelim', 'Preliminary'),
        ('final', 'Final'),
        ('practice', 'Practice'),
    ]
    name = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=15, choices=EXAM_TYPES)
    standard = models.CharField(max_length=100)
    academic_year = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    total_marks = models.IntegerField()
    passing_marks = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.standard}"


class Mark(models.Model):
    GRADE_CHOICES = [
        ('A+', 'A+'), ('A', 'A'), ('B+', 'B+'), ('B', 'B'),
        ('C', 'C'), ('D', 'D'), ('F', 'Fail')
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='marks')
    subject = models.CharField(max_length=100)
    marks_obtained = models.DecimalField(max_digits=6, decimal_places=2)
    grade = models.CharField(max_length=3, choices=GRADE_CHOICES, blank=True)
    is_absent = models.BooleanField(default=False)
    remarks = models.CharField(max_length=255, blank=True)
    entered_by = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'exam', 'subject')

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.marks_obtained}"
