"""fby_market URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from main.views import catalogue_list, offer_by_sku, account_login, account_register, offer_by_sku_edit

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', catalogue_list, name='catalogue_list'),

    path('api/v1/catalogue/', catalogue_list, name='catalogue_list'),
    path('api/v1/catalogue/<sku>/',  offer_by_sku, name='offer_by_sku'),
    path('api/v1/accounts/login/', account_login, name = 'account_login'),
    path('api/v1/account/register/', account_register, name = 'account_register'),
    path('api/v1/catalogue/<sku>/edit/', offer_by_sku_edit, name = 'offer_by_sku_edit')
]
