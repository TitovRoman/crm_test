from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic import ListView, CreateView, \
    UpdateView

from crm import forms
from crm import models
from crm.mixins import AdministratorMixin


class ClientBaseEditorView(SuccessMessageMixin):
    model = models.Client
    template_name = 'crm/client/client_create.html'
    form_class = forms.ClientForm
    redirect_url = 'home'

    def get_success_url(self):
        return reverse('client_edit', kwargs={'pk': self.object.id})


class ClientCreateView(AdministratorMixin, ClientBaseEditorView, CreateView):
    success_message = "Клиент создан"
    form_class = forms.ClientCreateForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['title'] = 'Новый клиент'

        return context


class ClientEditView(AdministratorMixin, ClientBaseEditorView, UpdateView):
    success_message = "Информация о клиенте обнавлена"
    form_class = forms.ClientEditForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['title'] = 'Изменение информации о клиенте'

        return context


class ClientsView(AdministratorMixin, ListView):
    model = models.Client
    context_object_name = 'clients'
    template_name = 'crm/client/clients_list.html'
    redirect_url = 'home'
