from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpRequest
from django.views import View


class BaseView(LoginRequiredMixin, View):
    """
    Базовый класс для отображения каталога
    """
    context = {}
    request = None

    def context_update(self, data: dict):
        self.context = {**data, **self.context}

    def save_models(self, request: HttpRequest) -> HttpResponse:
        for model in self.models_to_save:
            if not model(request=request).save():
                break
        return self.get(request=request)

    def end_it(self) -> HttpResponse:
        pass
