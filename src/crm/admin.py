from django.contrib import admin

from .models import Application, Client, Status, Category

admin.site.register(Application)
admin.site.register(Client)
admin.site.register(Status)
admin.site.register(Category)
