from django.contrib.auth.views import LoginView

from .forms import MyAuthenticationForm


class MyLoginView(LoginView):
    form_class = MyAuthenticationForm
    redirect_authenticated_user = True
    template_name = './authentication/login.html'
