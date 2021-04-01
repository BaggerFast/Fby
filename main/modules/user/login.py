from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from main.forms.user import UserLoginForm
from main.view import get_navbar, Page


class MyLoginFormView(FormView):
    """отображение авторизации"""
    form_class = UserLoginForm
    template_name = Page.login
    context = {'title': 'Login', 'page_name': 'Авторизация'}

    def get(self, request, *args, **kwargs):
        self.context['navbar'] = get_navbar(request)
        self.context['forms'] = self.get_context_data()['form']
        return self.render_to_response(self.context)

    def form_invalid(self, form):
        return self.get(self.request)

    def form_valid(self, form):
        user = authenticate(username=form.data.get('username'), password=form.data.get('password'))
        login(self.request, user)
        messages.success(self.request, 'Авторизация прошла успешно')
        return redirect(reverse('index'))
