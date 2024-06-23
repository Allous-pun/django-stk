
from django.db import models
from django.utils.translation import gettext_lazy as _

class Package(models.Model):
    PACKAGE_CHOICES = [
        ('data', 'Data'),
        ('sms', 'SMS'),
        ('calls', 'Calls'),
    ]

    name = models.CharField(max_length=10, choices=PACKAGE_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name