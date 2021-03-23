from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserLoginForm(AuthenticationForm):
    """Модель юзера для авторизации"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    """Модель юзера для регистрации"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2')
