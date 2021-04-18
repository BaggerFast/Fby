from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from fby_market.settings import MEDIA_URL
from django.contrib.auth.forms import PasswordChangeForm
from main.forms.user import UserChangeForm
from main.modules.base import BaseView
from main.view import get_navbar, Page
from main.models import User


class ProfileView(BaseView):
    context = {'title': 'Profile', 'page_name': 'Личный кабинет'}

    def get(self, request) -> HttpResponse:
        user = User.objects.get(username=request.user)
        local_context = {
            'navbar': get_navbar(request),
            'photo': f'{MEDIA_URL}/{user.image}',
            'user': user,
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
            'passwd_form': PasswordChangeForm(user=user),
        }
        self.context_update(local_context)
        return render(self.request, Page.profile_edit, self.context)

    def post(self, request):
        user = User.objects.get(username=request.user)
        message = form = None
        print(request.POST)
        if 'first_name' in request.POST:
            form = UserChangeForm(self.request.POST, self.request.FILES, instance=user)
            message = 'Данные успешно измененны'
        if 'old_password' in request.POST:
            form = PasswordChangeForm(user=user, data=request.POST)
            message = 'Пароль успешно поменян'
        if form.is_valid():
            form.save()
            messages.success(request, message)
        else:
            return self.get(request=request)
        return render(request, Page.profile, self.context)
