from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(default=0, null=False, blank=False)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    created_time = models.DateField(auto_now_add=True)

    def clean(self):
        if self.age < 16:
            raise ValidationError(
                "les Utilisateur de moin de 16 ans ne sont pas accepter")
        super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
