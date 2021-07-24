from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from .forms import SearchForm
from .models import Application


class BaseApplicationsView(ListView):
    model = Application
    context_object_name = 'applications'
    template_name = 'crm/application/applications_list.html'

    def dispatch(self, request, *args, **kwargs):
        self.search_form = SearchForm(request.GET)
        self.search_form.is_valid()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['applications_title'] = 'Ваши заявки'

        context['search_form'] = self.search_form

        return context


class AllApplicationsView(BaseApplicationsView):
    def get_queryset(self):
        return self.model.objects.all()


class EmployeeApplicationsView(BaseApplicationsView):
    def get_queryset(self):
        return (
            self.model.objects
            .filter(employee=self.request.user)
            .filter(creation_date__gt=self.search_form.cleaned_data['date_to'])
        )



