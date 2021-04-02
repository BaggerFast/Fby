from django.views.generic.edit import FormView
from main.view import get_navbar


class BaseView(FormView):
    context = None

    def get(self, request, *args, **kwargs):
        self.context['navbar'] = get_navbar(request)
        self.context['forms'] = self.get_context_data()['form']
        return self.render_to_response(self.context)

    def form_invalid(self, form):
        return self.get(self.request)
