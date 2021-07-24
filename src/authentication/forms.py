from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse


class MyAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Войти', css_class='btn btn-primary btn-lg btn-block'))
        self.helper.label_class = 'text-muted'

        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

        self.helper.layout = Layout('username', 'password')


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "password1", "password2")
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('register')
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Повторите пароль'

        self.helper.add_input(
            Submit(
                'submit',
                'Зарегистрироваться',
                css_class='btn btn-primary btn-lg btn-block'
                )
        )
