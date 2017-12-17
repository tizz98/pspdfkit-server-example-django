from django.contrib.auth import views

from pspdfkit_example.forms import SimpleLoginForm


class LoginView(views.LoginView):
    form_class = SimpleLoginForm
