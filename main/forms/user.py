from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, SetPasswordForm
from django.utils.translation import gettext, gettext_lazy as _
from django import forms

import main
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
        labels = {'username': 'Логин'}


class SetEmailForm(forms.Form):
    """
    A form that lets a user change set their email
    """

    new_email = forms.EmailField(
        label=_("New email"),
        widget=forms.EmailInput(attrs={'autocomplete': 'new-email'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        if self.is_valid():
            self.user.email = self.data["new_email"]
            if commit:
                self.user.save()
            return self.user


class SetImageForm(forms.Form):
    """
        A form that lets a user change set their email
    """

    image = forms.ImageField()

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        self.user.image = self.files["image"]
        if commit:
            self.user.save()
        return self.user
