from django.contrib.auth import login, authenticate
from django.views.generic.edit import FormView
from main.models.user.registration import UserRegistrationForm
from django.urls import reverse
from django.shortcuts import redirect
from main.views import Page


class MyRegisterFormView(FormView):
    form_class = UserRegistrationForm
    template_name = Page.registration

    def form_valid(self, form):
        form.save()
        user = authenticate(username=form.data.get('username'), password=form.data.get('password2'))
        login(self.request, user)
        return redirect(reverse('index'))

    def form_invalid(self, form):
        return super(MyRegisterFormView, self).form_invalid(form)
