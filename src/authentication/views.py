from django.conf import settings
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

from .forms import MyUserCreationForm, MyAuthenticationForm


class MyRegisterView(CreateView):
    form_class = MyUserCreationForm
    success_url = settings.LOGIN_URL
    template_name = './authentication/register.html'


class MyLoginView(LoginView):
    form_class = MyAuthenticationForm
    redirect_authenticated_user = True
    template_name = './authentication/login.html'
