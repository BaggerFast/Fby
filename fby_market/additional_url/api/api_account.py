from main.views import account_login, account_register
from django.urls import path

urlpatterns = [
    path('accounts/login/', account_login, name='account_login'),
    path('account/register/', account_register, name='account_register'),
    ]
