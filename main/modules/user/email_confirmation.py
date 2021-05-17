from django.http import HttpResponse
from main.modules.base import BaseView
from main.view import get_navbar, Page
from django.shortcuts import render
from django_email_verification import send_email


class EmailConfirmation(BaseView):
    context = {'title': 'EmailConfirm', 'page_name': 'Подтвердить почту'}

    def get(self, request) -> HttpResponse:
        user = request.user
        user.is_active = False
        send_email(user)

        local_context = {
            'navbar': get_navbar(request),
        }
        self.context_update(local_context)

        return render(self.request, Page.profile, self.context)
