from django.shortcuts import render
from django.http import HttpResponse

from fby_market.settings import MEDIA_URL
from django.contrib.auth.forms import SetPasswordForm
from main.forms.user import SetEmailForm, SetImageForm, SetPasswordFormCustom, SetYMKeysForm
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

    def get_data(self, request):
        user = User.objects.get(username=request.user)
        local_context = {
            'navbar': get_navbar(request),
            'photo': f'{MEDIA_URL}/{user.image}',
            'user': user,
            'password_form': SetPasswordForm(user),
            'email_form': SetEmailForm(user),
            'image_form': SetImageForm(user),
        }
        self.context_update(local_context)

    def get(self, request) -> HttpResponse:
        self.get_data(request)
        return render(self.request, Page.profile_edit, self.context)

    def post(self, request):
        if 'password' in request.POST:
            form = SetPasswordForm(user=request.user, data=request.POST)
        elif 'email' in request.POST:
            form = SetEmailForm(user=request.user, data=request.POST)
        elif 'image' in request.POST:
            form = SetImageForm(user=request.user, data=request.POST, files=request.FILES)

        if form.is_valid():
            form.save()
        self.get_data(request)
        return render(self.request, Page.profile_edit, self.context)
