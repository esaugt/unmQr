from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Los campos username, email y password, ya están incluidos en AbstactUser

    def __str__(self):
        return self.username


