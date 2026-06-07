from django.db import models
from apps.accounts.models import User


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile',
                                null=True, blank=True)
    full_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    alternate_phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True)
    annual_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    address = models.TextField()
    relation = models.CharField(max_length=50, default='Father')

    def __str__(self):
        return self.full_name


class Student(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    BLOOD_GROUPS = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    BLOOD_GROUP_CHOICES = [(bg, bg) for bg in BLOOD_GROUPS]
    STANDARD_CHOICES = [
        ('1', '1st Standard'),
        ('2', '2nd Standard'),
        ('3', '3rd Standard'),
        ('4', '4th Standard'),
        ('5', '5th Standard'),
        ('6', '6th Standard'),
        ('7', '7th Standard'),
        ('8', '8th Standard'),
        ('9', '9th Standard'),
        ('10', '10th Standard'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=255)
    standard = models.CharField(max_length=10, choices=STANDARD_CHOICES, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='students/photos/', blank=True, null=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True)
    roll_number = models.CharField(max_length=20)
    mobile_number = models.CharField(max_length=15, blank=True)
    school_name = models.CharField(max_length=255, blank=True)
    address = models.TextField()
    admission_date = models.DateField()
    receive_admin_alerts = models.BooleanField(default=True, help_text='Whether this student should receive admin alerts and daily notifications')
    notes_access_enabled = models.BooleanField(
        default=True,
        help_text='Disable to hide and block Chapter-wise Notes for this student.',
    )
    question_papers_access_enabled = models.BooleanField(
        default=True,
        help_text='Disable to hide and block Question Papers for this student.',
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['roll_number']

    def __str__(self):
        return f"{self.full_name} ({self.student_id})"


class StandardFeatureAccess(models.Model):
    standard = models.CharField(
        max_length=10,
        choices=Student.STANDARD_CHOICES,
        unique=True,
    )
    notes_enabled = models.BooleanField(
        default=True,
        help_text='Enable or disable Chapter-wise Notes for this standard.',
    )
    question_papers_enabled = models.BooleanField(
        default=True,
        help_text='Enable or disable Question Papers for this standard.',
    )

    class Meta:
        verbose_name = 'Standard Feature Access'
        verbose_name_plural = 'Standard Feature Access'
        ordering = ['standard']

    def __str__(self):
        return f"Std {self.standard}: notes={'ON' if self.notes_enabled else 'OFF'}, papers={'ON' if self.question_papers_enabled else 'OFF'}"
