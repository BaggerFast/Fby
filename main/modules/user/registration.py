from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.views.generic.edit import FormView
from django.urls import reverse
from django.shortcuts import redirect
from main.forms.user import UserRegistrationForm
from main.view import get_navbar, Page


class MyRegisterFormView(FormView):
    """отображение регистрации"""

    form_class = UserRegistrationForm
    template_name = Page.registration
    context = {'title': 'Registration', 'page_name': 'Регистрация'}

    def get(self, request, *args, **kwargs):
        self.context['navbar'] = get_navbar(request)
        self.context['forms'] = self.get_context_data()['form']
        return self.render_to_response(self.context)

    def form_invalid(self, form):
        return self.get(self.request)

    def form_valid(self, form):
        form.save()
        user = authenticate(username=form.data.get('username'), password=form.data.get('password2'))
        login(self.request, user)
        messages.success(self.request, 'Вы успешно зарегистрировались!')
        return redirect(reverse('index'))
