from django.db import models
import uuid
from accounts.models import CustomUser
from project.models import Project


class Issue(models.Model):
    STATUE_CHOICES = [
        ('Todo', 'To do'),
        ('InProgress', 'In progress'),
        ('Finished', 'Finished'),
    ]
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    TAG_CHOICES = [
        ('Bug', 'Bug'),
        ('Feature', 'Feature'),
        ('Task', 'Task'),
    ]
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="issue_author", verbose_name="Auteur du ticket")
    assign_to = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True, related_name="assigned_user",
        limit_choices_to={'contributor__project': models.F('project')},
        verbose_name="assigner à"
    )
    project = models.ForeignKey(Project, null=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, null=False)
    description = models.TextField(
        max_length=500, verbose_name="Description ticket")
    statue = models.CharField(
        max_length=12, choices=STATUE_CHOICES, verbose_name="statue")
    priority = models.CharField(
        max_length=12, choices=PRIORITY_CHOICES, verbose_name="priorité")
    tag = models.CharField(
        max_length=12, choices=TAG_CHOICES, verbose_name="tag")
    created_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True, related_name="comment_author",
        verbose_name="Auteur du commentaire",
    )
    issue = models.ForeignKey(
        Issue, null=False, on_delete=models.CASCADE, verbose_name="Ticket")
    description = models.TextField(
        max_length=500, verbose_name="commentaire")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return 'commentaire de : ' + self.author
