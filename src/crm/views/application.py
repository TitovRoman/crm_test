from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView, \
    UpdateView

from crm import forms
from crm import models
from crm.mixins import AdministratorMixin, \
    AdministratorOrModelEmployeeMixin
from crm.services.search_in_applications import SearchInApplicationsHandler


class BaseApplicationsView(ListView):
    model = models.Application
    context_object_name = 'applications'
    template_name = 'crm/application/applications_list.html'
    redirect_url = 'home'

    def dispatch(self, request, *args, **kwargs):
        self.search_form = forms.SearchForm(request.GET)
        self.search_form.is_valid()

        self.search_handler = SearchInApplicationsHandler(
            self.search_form.cleaned_data,
        )

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['search_form'] = self.search_form

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.search_handler.get_query()
        return queryset.filter(search_query).all_select_related()


class AllApplicationsView(AdministratorMixin, BaseApplicationsView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['applications_title'] = 'Все заявки'

        return context


class EmployeeApplicationsView(LoginRequiredMixin, BaseApplicationsView):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(employee=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['applications_title'] = 'Ваши заявки'

        return context


class ApplicationBaseEditorView(SuccessMessageMixin):
    model = models.Application
    template_name = 'crm/application/application_create.html'
    form_class = forms.ApplicationForm
    redirect_url = 'home'

    def get_success_url(self):
        return reverse('application', kwargs={'pk': self.object.id})


class ApplicationView(AdministratorOrModelEmployeeMixin, View):
    model = models.Application
    context_object_name = 'application'
    template_name = 'crm/application/application.html'
    redirect_url = 'home'

    def get(self, request, *args, **kwargs):
        application = get_object_or_404(self.model, id=kwargs['pk'])
        context = {
            'application': application,
        }

        if 'new_status' not in request.GET:
            status_form = forms.ChangeStatusForm({
                'new_status': application.status.id,
            })
        else:
            status_form = forms.ChangeStatusForm(request.GET)

        if status_form.is_valid():
            current_status = application.status
            status_from_form = status_form.cleaned_data['new_status']
            if current_status != status_from_form:
                messages.success(self.request, 'Статус обнавлен')
                application.status = status_from_form
                application.save()

        context['change_status_form'] = status_form

        return render(request, self.template_name, context=context)


class ApplicationCreateView(
    AdministratorMixin,
    ApplicationBaseEditorView,
    CreateView,
):
    success_message = "Заявка создана"
    form_class = forms.ApplicationCreateForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['title'] = 'Новая заявка'

        return context


class ApplicationEditView(
    AdministratorOrModelEmployeeMixin,
    ApplicationBaseEditorView,
    UpdateView,
):
    success_message = "Заявка изменена"
    form_class = forms.ApplicationEditForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['title'] = f'Изменение заявки №{self.object.id}'

        return context
