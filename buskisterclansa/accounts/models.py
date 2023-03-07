from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    is_admin = models.BooleanField(default=False, null=False)
