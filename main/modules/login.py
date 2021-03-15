from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from django.urls import reverse
from django.shortcuts import redirect
from main.models.user.login import UserLoginForm
from main.views import Page


class MyLoginFormView(FormView):
    form_class = UserLoginForm
    template_name = Page.login

    def form_valid(self, form):
        user = authenticate(username=form.data.get('username'), password=form.data.get('password'))
        login(self.request, user)
        return redirect(reverse('index'))

    def form_invalid(self, form):
        return super(MyLoginFormView, self).form_invalid(form)
