from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from authentication.views import MyRegisterView, MyLoginView
from crm.views.application import EmployeeApplicationsView, \
    AllApplicationsView, ApplicationCreateView, ApplicationView, \
    ApplicationEditView
from crm.views.client import ClientCreateView, ClientEditView, ClientsView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', MyLoginView.as_view(), name='login'),
    path('register/', MyRegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('', EmployeeApplicationsView.as_view(), name='home'),
    path(
        'applications/all/',
        AllApplicationsView.as_view(),
        name='all_applications',
    ),
    path(
        'applications/<int:pk>/',
        ApplicationView.as_view(),
        name='application'
    ),
    path(
        'applications/edit/<int:pk>/',
        ApplicationEditView.as_view(),
        name='application_edit'
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
