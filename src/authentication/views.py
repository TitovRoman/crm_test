from django.conf import settings
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

from .forms import MyUserCreationForm, MyAuthenticationForm


class MyLoginView(LoginView):
    form_class = MyAuthenticationForm
    redirect_authenticated_user = True
    template_name = './authentication/login.html'
