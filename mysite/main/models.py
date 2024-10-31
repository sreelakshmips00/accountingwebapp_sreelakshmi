from django.db import models
from decimal import Decimal
from datetime import date


class Expense(models.Model):
    TAX_RATES = {
        'IGST': 18.00,  # Percentage for IGST
        'CGST': 0.09,   # Percentage for CGST 
        'KGST': 0.09,   # Percentage for KGST 
        'TDS': 10.00,   # Percentage for TDS
    }

    date = models.DateField()
    party = models.CharField(max_length=100)
    particulars = models.TextField()
    invoice_no = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    bank_cash = models.CharField(max_length=10, choices=[('Bank', 'Bank'), ('Cash', 'Cash')], default='Cash')
    igst = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    cgst = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    kgst = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tds = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField(max_digits=14, decimal_places=2, blank=True, default=Decimal('0.00'))  

    def save(self, *args, **kwargs):
        if self.amount:
            
            self.total = self.amount + (self.amount * self.igst / 100) + \
                         (self.amount * self.cgst / 100) + (self.amount * self.kgst / 100) + \
                         (self.amount * self.tds / 100)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.invoice_no} - {self.party}"
