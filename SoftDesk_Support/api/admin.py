from django.contrib import admin

# Register your models here.
from project.models import Project, Contributor
from issue.models import Issue, Comment

admin.site.register(Project)
admin.site.register(Contributor)
admin.site.register(Issue)
admin.site.register(Comment)
