from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class Func:
    fields = dict()

    def execute(self):
        for key in self.fields.keys():
            self.fields[key].widget.attrs['class'] = 'form-control'


class UserLoginForm(AuthenticationForm, Func):
    """Модель юзера для авторизации"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.execute()

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm, Func):
    """Модель юзера для регистрации"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.execute()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2')
