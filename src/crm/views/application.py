from django.urls import reverse
from django.views.generic import ListView, CreateView, \
    DetailView, UpdateView

from crm import forms
from crm import models


class BaseApplicationsView(ListView):
    model = models.Application
    context_object_name = 'applications'
    template_name = 'crm/application/applications_list.html'

    def dispatch(self, request, *args, **kwargs):
        self.search_form = forms.SearchForm(request.GET)
        self.search_form.is_valid()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['search_form'] = self.search_form

        return context


class AllApplicationsView(BaseApplicationsView):
    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['applications_title'] = 'Все заявки'

        return context


class EmployeeApplicationsView(BaseApplicationsView):
    def get_queryset(self):
        return (
            self.model.objects
            .filter(employee=self.request.user)
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['applications_title'] = 'Ваши заявки'

        return context


class ApplicationView(DetailView):
    model = models.Application
    context_object_name = 'application'
    template_name = 'crm/application/application.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['change_status_form'] = forms.ChangeStatusForm({'new_status': self.object.status.id})

        return context


class ApplicationCreateView(CreateView):
    model = models.Application
    template_name = 'crm/application/application_create.html'
    form_class = forms.ApplicationForm
    redirect_url = 'application_create'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['title'] = 'Создание заявки'

        return context

    def get_success_url(self):
        return reverse('application', kwargs={'pk': self.object.id})


class ApplicationEditView(UpdateView):
    model = models.Application
    template_name = 'crm/application/application_create.html'
    form_class = forms.ApplicationForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['title'] = f'Изменение заявки №{self.object.id}'

        return context