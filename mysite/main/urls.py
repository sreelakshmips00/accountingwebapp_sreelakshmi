from django.urls import path
from . import views
from .views import home, create,invoice,receipt, expenses, view_expenses, add_expenses, accounts, manage, profile, logout
from django.urls import path
from . import views



urlpatterns = [
    path('', home, name='dashboard'),  # This will render the dashboard
    path('create/', create, name='create'),
    path('create-invoice/', views.invoice, name='create_invoice'),
    path('create-receipt/', views.receipt, name='create_receipt'),
    path('expenses/', expenses, name='expenses'),
    path('add_expenses/', views.add_expenses, name='add_expenses'),
    path('view_expenses/', views.view_expenses, name='view_expenses'),
    path('accounts/', accounts, name='accounts'),
    path('manage/', manage, name='manage'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
]