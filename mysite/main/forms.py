from django import forms
from .models import Expense
import datetime



class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['date', 'party', 'particulars', 'invoice_no', 'amount', 'bank_cash']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


YEAR_CHOICES = [(year, year) for year in range(2017, datetime.datetime.now().year + 1)]
MONTH_CHOICES = [
    (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
    (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
    (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
]

class ExpenseFilterForm(forms.Form):
    year = forms.ChoiceField(choices=YEAR_CHOICES, required=True, label='Year')
    month = forms.ChoiceField(choices=MONTH_CHOICES, required=True, label='Month')
