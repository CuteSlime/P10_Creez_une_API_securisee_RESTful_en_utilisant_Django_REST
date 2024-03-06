from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(default=0, null=False, blank=False)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    created_time = models.DateField(auto_now_add=True)

    def clean(self):
        if self.age < 16 and (self.can_be_contacted or self.can_data_be_shared):
            raise ValidationError(
                "En respect du RGPD, les Utilisateur de moin de "
                + "16 ans ne peuvent pas être contacter ni partager leur information")
        super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
