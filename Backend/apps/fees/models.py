from django.db import models
from apps.students.models import Student


class FeeStructure(models.Model):
    TERM_CHOICES = [('Q1', 'Q1'), ('Q2', 'Q2'), ('Q3', 'Q3'), ('Q4', 'Q4'),
                    ('Annual', 'Annual'), ('Monthly', 'Monthly')]
    standard = models.CharField(max_length=100)
    academic_year = models.CharField(max_length=100)
    term = models.CharField(max_length=10, choices=TERM_CHOICES)
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    exam_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    library_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sports_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_date = models.DateField()

    @property
    def total_fee(self):
        return (self.tuition_fee + self.exam_fee + self.library_fee +
                self.sports_fee + self.other_fee)

    def __str__(self):
        return f"{self.standard} - {self.term} ({self.academic_year})"


class Fee(models.Model):
    STATUS_CHOICES = [('paid', 'Paid'), ('unpaid', 'Unpaid'), ('partial', 'Partial')]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    number_of_installments = models.PositiveIntegerField(null=True, blank=True)
    next_installment_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpaid')
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def remaining_fee(self):
        return self.total_fee - self.amount_paid

    @property
    def balance(self):
        return self.remaining_fee

    def __str__(self):
        return f"{self.student} - {self.total_fee} ({self.status})"


class FeeReceipt(models.Model):
    PAYMENT_MODES = [('Cash', 'Cash'), ('Online', 'Online'), ('Cheque', 'Cheque'),
                     ('DD', 'Demand Draft'), ('UPI', 'UPI')]
    receipt_number = models.CharField(max_length=50, unique=True)
    fee = models.ForeignKey(Fee, on_delete=models.CASCADE, related_name='receipts')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_MODES)
    transaction_id = models.CharField(max_length=100, blank=True)
    receipt_pdf = models.FileField(upload_to='receipts/', blank=True, null=True)
    issued_by = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Receipt #{self.receipt_number} - {self.fee.student}"
