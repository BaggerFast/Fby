from django.shortcuts import render
from django.http import HttpResponse

from fby_market.settings import MEDIA_URL
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
