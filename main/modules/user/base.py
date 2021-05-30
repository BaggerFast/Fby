from django.views.generic.edit import FormView
from main.view import Navbar


class BaseView(FormView):
    context = None

    def context_update(self, data: dict):
        self.context.update(data)

    def get(self, request, *args, **kwargs):
        self.context_update({'navbar': Navbar(request).get(), 'form': self.get_context_data()['form']})
        return self.render_to_response(self.context)

    def form_invalid(self, form):
        return self.get(self.request)
