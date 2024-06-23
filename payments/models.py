from django.db import models

class Transaction(models.Model):
    PACKAGE_CHOICES = [
        ('data', 'Data'),
        ('sms', 'SMS'),
        ('calls', 'Calls'),
    ]

    package = models.CharField(max_length=10, choices=PACKAGE_CHOICES)
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} - {self.package} - {self.amount}"