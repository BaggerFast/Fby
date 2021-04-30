from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from main.forms.user import UserChangeForm, UserPasswordChangeForm
from main.modules.base import BaseView
from main.view import get_navbar, Page
from main.models import User
from django.shortcuts import render, redirect
from django.urls import reverse


class ProfileView(BaseView):
    context = {'title': 'Profile', 'page_name': 'Личный кабинет'}

    def get(self, request) -> HttpResponse:
        user = User.objects.get(username=request.user)
        local_context = {
            'navbar': get_navbar(request),
            'base_form': UserChangeForm(instance=user, disable=True),
        }
        self.context_update(local_context)
        return render(self.request, Page.profile, self.context)


class ProfileEditView(BaseView):
    context = {'title': 'Profile edit', 'page_name': 'Редактирование профиля'}

    def get(self, request) -> HttpResponse:
        user = User.objects.get(username=request.user)
        local_context = {
            'navbar': get_navbar(request),
            'base_form': UserChangeForm(instance=user),
            'passwd_form': UserPasswordChangeForm(user=user),
        }
        self.context_update(local_context)
        return render(self.request, Page.profile_edit, self.context)

    def post(self, request):
        user = User.objects.get(username=request.user)
        msg = form = None
        if 'first_name' in request.POST:
            form = UserChangeForm(self.request.POST, self.request.FILES, instance=user)
            msg = 'Данные успешно изменены'
        if 'old_password' in request.POST:
            form = PasswordChangeForm(user=user, data=request.POST)
            msg = 'Пароль успешно поменян'
        if form.is_valid():
            form.save()
            messages.success(request, msg)
            return redirect(reverse('profile'))
        else:
            messages.error(request, 'Ошибка')
        return self.get(request=request)
