from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView
from main.models.registration import UserRegistrationForm
# Вариант регистрации на базе класса FormView


class MyRegisterFormView(FormView):
    form_class = UserRegistrationForm
    success_url = 'catalogue/'
    template_name = 'pages/registration.html'

    def form_valid(self, form):
        form.save()
        return redirect(reverse('catalogue_list'))

    def form_invalid(self, form):
        return super(MyRegisterFormView, self).form_invalid(form)
