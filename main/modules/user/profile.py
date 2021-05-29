from django.http import HttpResponse
from django.contrib import messages
from main.forms.user import UserChangeForm, UserPasswordChangeForm
from main.modules.base import BaseView
from main.view import Navbar, Page
from main.models import User
from django.shortcuts import render, redirect
from django.urls import reverse


class ProfileView(BaseView):
    context = {'title': 'Аккаунт', 'page_name': 'Личный кабинет'}

    def get(self, request) -> HttpResponse:
        user = User.objects.get(username=request.user)
        local_context = {
            'navbar': Navbar(request).get(),
            'base_form': UserChangeForm(instance=user, disable=True),
        }
        self.context_update(local_context)
        return render(self.request, Page.profile, self.context)


class ProfileEditView(BaseView):
    context = {'title': 'Настройки аккаунта', 'page_name': 'Редактирование профиля'}

    def get(self, request) -> HttpResponse:
        user = User.objects.get(username=request.user)
        local_context = {
            'navbar': Navbar(request).get(),
            'base_form': UserChangeForm(instance=user),
            'passwd_form': UserPasswordChangeForm(user=user),
        }
        self.context_update(local_context)
        return render(self.request, Page.profile_edit, self.context)

    def post(self, request):
        user = User.objects.get(username=request.user)
        form = None
        if 'first_name' in request.POST:
            form = UserChangeForm(self.request.POST, self.request.FILES, instance=user)
        if 'old_password' in request.POST:
            form = UserPasswordChangeForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, form.success_message)
            return redirect(reverse('profile'))
        else:
            messages.error(request, 'Ошибка')
        return self.get(request=request)
