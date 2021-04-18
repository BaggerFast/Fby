from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm as Us
from django.utils.translation import gettext_lazy as _
from django import forms
from main.models import User


class Func:
    fields = dict()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.execute()

    def execute(self):
        for key in self.fields.keys():
            self.fields[key].widget.attrs['class'] = 'form-control'


class UserLoginForm(AuthenticationForm, Func):
    """Модель юзера для авторизации"""
    class Meta:
        model = User
        fields = ('username', 'password')
        labels = {'username': 'Логин'}


class UserRegistrationForm(UserCreationForm, Func):
    """Модель юзера для регистрации"""
    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password1', 'password2', 'image')
        labels = {'username': 'Логин', 'first_name': 'ФИО'}


class UserChangeForm(Us, Func):
    key1 = forms.CharField(label='1й токен', required=False)
    key2 = forms.CharField(label='2й токен', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del(self.fields['password'])

    class Meta:
        model = User
        fields = ('first_name', 'email', 'image')
        labels = {'username': 'Логин', 'first_name': 'ФИО'}
