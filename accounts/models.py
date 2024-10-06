from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, validators=[EmailValidator()])

    def __str__(self):
        return self.username