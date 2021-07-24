from django.urls import reverse
from django.views.generic import ListView, CreateView, \
    UpdateView

from crm import forms
from crm import models


class ClientCreateView(CreateView):
    model = models.Client
    template_name = 'crm/client/client_create.html'
    form_class = forms.ClientForm
    redirect_url = 'application_create'

    def get_success_url(self):
        return reverse('client_edit', kwargs={'pk': self.object.id})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['title'] = 'Новый клиент'

        return context


class ClientEditView(UpdateView):
    model = models.Client
    template_name = 'crm/client/client_create.html'
    form_class = forms.ClientForm
    redirect_url = 'application_create'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['title'] = 'Изменение информации о клиенте'

        return context


class ClientsView(ListView):
    model = models.Client
    context_object_name = 'clients'
    template_name = 'crm/client/clients_list.html'
