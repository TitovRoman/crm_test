from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Row, Column
from django import forms

from . import models


class ChangeStatusForm(forms.Form):
    new_status = forms.ModelChoiceField(
        queryset=models.Status.objects.all(),
        label='Статус заявки',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'Изменить статус заявки'))


class SearchForm(forms.Form):
    date_from = forms.DateField(
        label='С указанной даты (включительно)',
        input_formats=['%d/%m/%Y'],
        required=False,
        error_messages={'invalid': 'Неверная дата. Формат ввода: dd/mm/yyyy'},
    )
    date_to = forms.DateField(
        label='До указанной даты (включительно)',
        input_formats=['%d/%m/%Y'],
        required=False,
        error_messages={'invalid': 'Неверная дата. Формат ввода: dd/mm/yyyy'},
    )
    application_category = forms.ModelMultipleChoiceField(
        queryset=models.Category.objects.all(),
        label='Категория запроса',
        required=False,
    )
    application_status = forms.ModelMultipleChoiceField(
        queryset=models.Status.objects.all(),
        label='Статус запроса',
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'Submit'))

        self.helper.layout = Layout(
            Row(
                Fieldset(
                    'За период',
                    Row(
                        Column('date_from', css_class='col-xl-12 col-md-6 col-12'),
                        Column('date_to', css_class='col-xl-12 col-md-6 col-12'),
                    ),
                    css_class='col-12'
                ),
            ),
            Row(
                Column('application_category', css_class='col-xl-12 col-md-6 col-12'),
                Column('application_status', css_class='col-xl-12 col-md-6 col-12'),
            ),
        )


class ClientForm(forms.ModelForm):
    button_message = 'Отправить'

    class Meta:
        model = models.Client
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'tg_username',
        ]

    def __init__(self, *argc, **kwargs):
        super().__init__(*argc, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='col-12 col-md-6'),
                Column('last_name', css_class='col-12 col-md-6'),
            ),
            Row(
                Column('phone_number', css_class='col-12 col-md-6 col-lg-4'),
                Column('email', css_class='col-12 col-md-6 col-lg-4'),
                Column('tg_username', css_class='col-12 col-md-6 col-lg-4'),
            ),

            Submit('submit', self.button_message),
        )


class ClientCreateForm(ClientForm):
    button_message = 'Создать'


class ClientEditForm(ClientForm):
    button_message = 'Исправить'


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = models.Application
        fields = [
            'title',
            'description',
            'category',
            'client',
            'employee',
            'status',
        ]

    def __init__(self, *argc, **kwargs):
        super().__init__(*argc, **kwargs)

        self.fields['employee'].queryset = self.fields['employee'].queryset.filter(is_employee='True')

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            'title',
            'description',
            Row(
                Column('client', css_class='col-12 col-md-6'),
                Column('employee', css_class='col-12 col-md-6'),
            ),
            Row(
                Column('category', css_class='col-12 col-md-6'),
                Column('status', css_class='col-12 col-md-6'),
            ),

            Submit('submit', 'Сохранить'),
        )


class ApplicationCreateForm(ApplicationForm):
    button_message = 'Создать'


class ApplicationEditForm(ApplicationForm):
    button_message = 'Исправить'
