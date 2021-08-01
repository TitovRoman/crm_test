from django.urls import path

from .views.application import EmployeeApplicationsView, \
    AllApplicationsView, ApplicationCreateView, ApplicationView, \
    ApplicationEditView
from .views.client import ClientCreateView, ClientEditView, ClientsView

urlpatterns = [
    path('', EmployeeApplicationsView.as_view(), name='home'),
    path(
        'applications/all/',
        AllApplicationsView.as_view(),
        name='all_applications',
    ),
    path(
        'applications/<int:pk>/',
        ApplicationView.as_view(),
        name='application',
    ),
    path(
        'applications/edit/<int:pk>/',
        ApplicationEditView.as_view(),
        name='application_edit',
    ),
    path(
        'applications/create/',
        ApplicationCreateView.as_view(),
        name='application_create',
    ),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/', ClientEditView.as_view(), name='client_edit'),
    path('clients/all/', ClientsView.as_view(), name='all_clients'),
]
