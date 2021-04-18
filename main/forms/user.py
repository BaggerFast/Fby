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


class CustomSetForm(forms.Form):
    """
        Base form that lets a user change set their params
    """
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, commit):
        if commit:
            self.user.save()
        return self.user


class SetEmailForm(CustomSetForm):
    """
        A form that lets a user change set their email
    """

    new_email = forms.EmailField(
        label=_("New email"),
        widget=forms.EmailInput(attrs={'autocomplete': 'new-email'}),
    )

    def save(self, commit=True):
        self.user.email = self.cleaned_data["new_email"]
        return super().save(commit)


class SetImageForm(CustomSetForm):
    """
        A form that lets a user change set their email
    """

    image = forms.ImageField()

    def save(self, commit=True):
        self.user.image = self.cleaned_data["image"]
        return super().save(commit)


class SetYMKeysForm(CustomSetForm):
    """
        A form that lets a user change set their YM keys
    """

    key1 = forms.CharField()
    key2 = forms.CharField()

    def save(self, commit=True):
        key1 = self.cleaned_data['key1']
        key2 = self.cleaned_data['key2']
        print(key1, key2)
