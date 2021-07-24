from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_administrator = models.BooleanField()
    is_employee = models.BooleanField()
