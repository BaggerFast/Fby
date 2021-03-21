from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserLoginForm(AuthenticationForm):
    """Модель юзера для авторизации"""
    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    """Модель юзера для регистрации"""
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2')
