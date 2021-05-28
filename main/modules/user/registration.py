from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.shortcuts import redirect
from main.forms import UserRegistrationForm
from main.modules.user.base import BaseView
from main.view import Page


class MyRegisterFormView(BaseView):
    """отображение регистрации"""

    form_class = UserRegistrationForm
    template_name = Page.registration
    context = {'title': 'Registration', 'page_name': 'Регистрация'}

    def form_valid(self, form):
        form.save()
        user = authenticate(username=form.data.get('username'), password=form.data.get('password2'))
        login(self.request, user)
        messages.success(self.request, 'Вы успешно зарегистрировались!')
        return redirect(reverse('index'))
