from django.db import models
from decimal import Decimal

class Expense(models.Model):
    TAX_RATES = {
        'IGST': Decimal('18.00'),  
        'CGST': Decimal('0.0009'),  
        'KGST': Decimal('0.0009'),   
        'TDS': Decimal('10.00'),  
    }

    date = models.DateField()
    party = models.CharField(max_length=100)
    particulars = models.TextField()
    invoice_no = models.CharField(max_length=20)  
    amount = models.DecimalField(max_digits=15, decimal_places=2)  
    bank_cash = models.CharField(max_length=20, default='Cash')
    igst = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    cgst = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    kgst = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    tds = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField(max_digits=15, decimal_places=2, blank=True, default=Decimal('0.00'))

    def save(self, *args, **kwargs):
        if self.amount:
            amount = Decimal(self.amount)  
            igst_amount = (amount * Decimal(self.TAX_RATES['IGST']) / Decimal('100')).quantize(Decimal('0.01'))
            cgst_amount = (amount * Decimal(self.TAX_RATES['CGST']) / Decimal('100')).quantize(Decimal('0.01'))
            kgst_amount = (amount * Decimal(self.TAX_RATES['KGST']) / Decimal('100')).quantize(Decimal('0.01'))
            tds_amount = (amount * Decimal(self.TAX_RATES['TDS']) / Decimal('100')).quantize(Decimal('0.01'))

            self.igst = igst_amount
            self.cgst = cgst_amount
            self.kgst = kgst_amount
            self.tds = tds_amount

        
            self.total = (amount + igst_amount + cgst_amount + kgst_amount - tds_amount).quantize(Decimal('0.01'))
            
        super().save(*args, **kwargs)
