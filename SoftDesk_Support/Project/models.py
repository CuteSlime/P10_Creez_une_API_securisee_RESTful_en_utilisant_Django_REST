from django.db import models

from accounts.models import CustomUser


class Project(models.Model):
    TYPE_CHOICES = [
        ('Back-end', 'Back-end'),
        ('Front-end', 'Front-end'),
        ('iOS', 'iOS'),
        ('Android', 'Android'),
    ]
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="Auteur du projet")
    contributors = models.ManyToManyField(
        CustomUser, through='Contributor', verbose_name="Contributeurs")
    name = models.CharField(max_length=60, null=False,
                            verbose_name="Nom du projet")
    description = models.TextField(
        max_length=500, verbose_name="Description du projet")
    type = models.CharField(
        max_length=10, choices=TYPE_CHOICES, verbose_name="type de projet")
    created_time = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.name


class Contributor(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_time = models.DateField(auto_now_add=True)
