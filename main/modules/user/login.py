from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.shortcuts import redirect
from main.forms.user import UserLoginForm
from main.modules.user.base import BaseView
from main.view import Page


class MyLoginFormView(BaseView):
    """отображение авторизации"""
    form_class = UserLoginForm
    template_name = Page.login
    context = {'title': 'Login', 'page_name': 'Авторизация'}

    def form_valid(self, form):
        user = authenticate(username=form.data.get('username'), password=form.data.get('password'))
        login(self.request, user)
        messages.success(self.request, 'Авторизация прошла успешно')
        return redirect(reverse('index'))
