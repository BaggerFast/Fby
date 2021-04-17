"""fby_market URL Configuration

The `urlpatterns` list routes URLs to view. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function view
    1. Add an import:  from my_app import view
    2. Add a URL to urlpatterns:  path('', view.home, name='home')
Class-based view
    1. Add an import:  from other_app.view import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from main.modules import *
import fby_market.additional_url.api.api_catalogue as catalogue
import fby_market.additional_url.api.api_orders as orders
from main.view.others import save_db_from_files, orders_list

urlpatterns = [
    path('', MainView.as_view(), name="index"),
    path('admin/', admin.site.urls),
    path('catalogue/', include(catalogue)),
    path('orders/', include(orders)),
    path('register/', MyRegisterFormView.as_view(), name="register"),
    path('login/', MyLoginFormView.as_view(), name='login'),
    path('logout/', login_required(LogoutView.as_view()), name='logout'),
    path('db_save/', save_db_from_files),
    path('temp/', orders_list)
]
