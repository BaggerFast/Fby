from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from main.modules.user import MyRegisterFormView, MyLoginFormView

urlpatterns = [
    path('register/', MyRegisterFormView.as_view(), name="register"),
    path('login/', MyLoginFormView.as_view(), name='login'),
    path('logout/', login_required(LogoutView.as_view()), name='logout'),
]
