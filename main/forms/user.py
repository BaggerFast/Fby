import os
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm as Us, PasswordChangeForm
from django import forms
from fby_market.settings import MEDIA_ROOT
from main.models import User


class Func:
    fields = dict()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.turn_off()

    def turn_off(self):
        for key in self.fields.keys():
            self.fields[key].widget.attrs['class'] = 'form-control'


class UserLoginForm(AuthenticationForm, Func):
    """Модель юзера для авторизации"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.turn_off()

    class Meta:
        model = User
        fields = ('username', 'password')
        labels = {'username': 'Логин'}


class UserRegistrationForm(UserCreationForm, Func):
    """Модель юзера для регистрации"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.turn_off()

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password1', 'password2', 'image')
        labels = {'username': 'Логин', 'first_name': 'ФИО'}


class UserChangeForm(Us, Func):
    key1 = forms.CharField(label='1й токен', required=False)
    key2 = forms.CharField(label='2й токен', required=False)

    def __init__(self, *args, **kwargs):
        self.del_old_image(args, kwargs['instance'])
        super().__init__(*args, **kwargs)
        self.turn_off()
        del (self.fields['password'])

    @staticmethod
    def del_old_image(args, user):
        if args and 'image' in args[1].keys() and str(user.image) != f'base/base.png':
            try:
                os.remove((MEDIA_ROOT + '/' + str(user.image)).replace('\\', '/'))
                os.rmdir((MEDIA_ROOT + '/' + str(user.username)).replace('\\', '/'))
            except FileNotFoundError:
                pass

    @staticmethod
    def check_image(instance):
        if not instance.image:
            instance.image = f'base/base.png'
            instance.save()
        return instance

    class Meta:
        model = User
        fields = ('first_name', 'email', 'image')
        labels = {'username': 'Логин', 'first_name': 'ФИО'}

    def save(self, commit=True):
        return self.check_image(super().save(commit=commit))


class UserPasswordChangeForm(PasswordChangeForm, Func):
    """Модель юзера для смены пароля"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.turn_off()
