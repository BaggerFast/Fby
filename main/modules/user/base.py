from django.http import HttpResponse
from django.views.generic.edit import FormView
from main.view import get_navbar


class BaseView(FormView):
    context = None

    def context_update(self, data: dict):
        self.context = {**data, **self.context}

    def get(self, request, *args, **kwargs):
        self.context_update({'navbar': get_navbar(request), 'form': self.get_context_data()['form']})
        return self.render_to_response(self.context)

    def form_invalid(self, form):
        return self.get(self.request)
