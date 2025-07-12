from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class Student(models.Model):
    TRADE_CHOICES = [
        ('Electrician', 'Electrician'),
        ('Fitter', 'Fitter'),
    ]
    student_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20, unique=True)
    adharcard_no = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    date_of_admission = models.DateField()
    trade = models.CharField(max_length=20, choices=TRADE_CHOICES)
    mobile_no = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    total_fees = models.IntegerField()

    def __str__(self):
        return f"{self.student_name} S/O {self.father_name} ({self.roll_no})"

    @property
    def fees_paid(self):
        return sum(fee.amount for fee in self.fees_set.all())

    @property
    def pending_fees(self):
        return self.total_fees - self.fees_paid

    @property
    def batch_year(self):
        return f"{self.date_of_admission.year} -{int(self.date_of_admission.year)+2}"


class Fees(models.Model):
    PAYMENT_MODE_CHOICES = [
        ('Cash', 'Cash'),
        ('Online', 'Online'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    fees_receipt_no = models.CharField(max_length=15, unique=True)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE_CHOICES)
    collected_by = models.ForeignKey(User, on_delete=models.PROTECT)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Fees"  # Singular name
        verbose_name_plural = "Fees"  # Plural name

    def __str__(self):
        return f"{self.student.student_name} - {self.amount} on {self.date}"
