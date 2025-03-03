from django.shortcuts import render, redirect
from django.utils.timezone import now
from .forms import ExpenseFilterForm
from .models import Expense
from .forms import ExpenseForm
from datetime import datetime
from decimal import Decimal
from decimal import Decimal, InvalidOperation
from django.http import HttpResponse
from decimal import Decimal
from django.template.loader import get_template



def home(request):
    return render(request, 'mysite/dashboard.html')

def create(request):
    return render(request, 'mysite/create.html')

def invoice(request):
    return render(request, 'mysite/create_invoice.html')

def receipt(request):
    return render(request, 'mysite/create_receipt.html')

def expenses(request):
    return render(request, 'mysite/expenses.html')

IGST_RATE = Decimal('0.18')  
CGST_RATE = Decimal('0.0009')  
KGST_RATE = Decimal('0.0009')  
TDS_RATE = Decimal('0.10')   

def add_expenses(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            try:
                amount = form.cleaned_data['amount']
                
                if amount <= Decimal('0.00'):
                    form.add_error('amount', 'Amount must be greater than zero.')
                else:
                    IGST_RATE = Decimal('18.00')  
                    CGST_RATE = Decimal('0.0009') 
                    KGST_RATE = Decimal('0.0009')  
                    TDS_RATE = Decimal('10.00')   

                    igst_amount = (amount * IGST_RATE / Decimal('100')).quantize(Decimal('0.01'))
                    cgst_amount = (amount * CGST_RATE / Decimal('100')).quantize(Decimal('0.01'))
                    kgst_amount = (amount * KGST_RATE / Decimal('100')).quantize(Decimal('0.01'))
                    tds_amount = (amount * TDS_RATE / Decimal('100')).quantize(Decimal('0.01'))
                    
                    total = (amount + igst_amount + cgst_amount + kgst_amount - tds_amount).quantize(Decimal('0.01'))

                    expense = form.save(commit=False)
                    expense.igst = igst_amount
                    expense.cgst = cgst_amount
                    expense.kgst = kgst_amount
                    expense.tds = tds_amount
                    expense.total = total  
                    expense.save()

                    return redirect('view_expenses')
            except InvalidOperation:
                form.add_error('amount', 'Invalid amount entered. Please check your inputs.')

    else:
        form = ExpenseForm()
    
    return render(request, 'mysite/add_expenses.html', {'form': form})


def view_expenses(request):
    current_year = now().year
    current_month = now().month

   
    if request.method == 'POST':
        form = ExpenseFilterForm(request.POST)
        if form.is_valid():
            selected_year = int(form.cleaned_data['year'])
            selected_month = int(form.cleaned_data['month'])
        else:
            selected_year = current_year
            selected_month = current_month
    else:
        form = ExpenseFilterForm(initial={'year': current_year, 'month': current_month})
        selected_year = current_year
        selected_month = current_month

    
    expenses = Expense.objects.filter(date__year=selected_year, date__month=selected_month)

    context = {
        'form': form,
        'expenses': expenses,
        'selected_year': selected_year,
        'selected_month': selected_month,
    }
    return render(request, 'mysite/view_expenses.html', context)



def accounts(request):
    return render(request, 'mysite/accounts.html')

def manage(request):
    return render(request, 'mysite/manage.html')

def profile(request):
    return render(request, 'mysite/profile.html')

def logout(request):
    return render(request, 'mysite/logout.html')
