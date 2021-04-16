from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View


class BaseView(LoginRequiredMixin, View):
    """
    Базовый класс для отображения каталога
    """
    context = {}
    request = None

    def context_update(self, data: dict):
        self.context = {**data, **self.context, }

    def end_it(self) -> HttpResponse:
        pass
