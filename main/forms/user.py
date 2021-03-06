import os
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm as Us, PasswordChangeForm
from fby_market.settings import MEDIA_ROOT
from main.models import User


class Func:
    fields = dict()

    disabled = []

    def turn_off(self, disable: bool = False):
        for key in self.fields.keys():
            self.fields[key].widget.attrs['class'] = 'form-control'
            self.fields[key].widget.attrs['placeholder'] = 'Не задано'
            if key in self.disabled or disable:
                self.fields[key].widget.attrs['disabled'] = 'true'


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
        fields = ('first_name', 'username', 'password1', 'password2', 'image', 'client_id', 'token', 'shop_id')
        labels = {'username': 'Логин', 'first_name': 'ФИО'}


class UserChangeForm(Us, Func):
    """Модель юзера для изменения данных"""
    def __init__(self, *args, **kwargs):
        self.del_old_image(args, kwargs['instance'])
        disabled = False
        if 'disable' in kwargs.keys():
            disabled = kwargs['disable']
            del kwargs['disable']
        super().__init__(*args, **kwargs)
        self.turn_off(disabled)
        del (self.fields['password'])

    @staticmethod
    def del_old_image(args, user):
        """Метод для удаления старой картинки, в случае её изменения"""
        if args and 'image' in args[1].keys() and str(user.image) != f'base/base.png':
            try:
                os.remove((MEDIA_ROOT + '/' + str(user.image)).replace('\\', '/'))
                os.rmdir((MEDIA_ROOT + '/' + str(user.username)).replace('\\', '/'))
            except FileNotFoundError:
                pass

    @staticmethod
    def check_image(instance):
        """Метод для проверки наличия картинки у юзера"""
        if not instance.image:
            instance.image = f'base/base.png'
            instance.save()
        return instance

    class Meta:
        model = User
        fields = ('first_name', 'image', 'client_id', 'token', 'shop_id')
        labels = {'username': 'Логин', 'first_name': 'ФИО'}

    def save(self, commit=True):
        return self.check_image(super().save(commit=commit))

    @property
    def success_message(self):
        return 'Данные успешно изменены'


class UserPasswordChangeForm(PasswordChangeForm, Func):
    """Модель юзера для смены пароля"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.turn_off()

    @property
    def success_message(self):
        return 'пароль успешно изменен'
