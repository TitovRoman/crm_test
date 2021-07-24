from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset
from django import forms
from django.forms import SelectDateWidget, SplitDateTimeWidget
from . import models


class SearchForm(forms.Form):
    date_from = forms.DateField(
        label='С указанной даты (включительно)',
        input_formats=['%d/%m/%Y'],
        required=False
    )
    date_to = forms.DateField(
        label='До указанной даты (включительно)',
        input_formats=['%d/%m/%Y'],
        required=False,
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
            Fieldset(
                'За период',
                'date_from',
                'date_to',
            ),
            'application_category',
            'application_status',
        )
