from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


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
        labels = {
            'username': 'Логин'
        }


class UserRegistrationForm(UserCreationForm, Func):
    """Модель юзера для регистрации"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.execute()

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Логин'
        }
