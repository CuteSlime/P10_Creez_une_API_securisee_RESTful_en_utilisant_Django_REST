from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import Group

from accounts.models import CustomUser
from project.models import Project, Contributor
from issue.models import Issue, Comment
from .serializers import (
    UserSerializer,
    GroupSerializer,
    ProjectSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer,
)
from .permissions import CustomUserPermissions, ProjectPermissions, IssuePermissions, CommentPermissions


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (CustomUserPermissions,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class GroupsViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [ProjectPermissions]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        contributor_name = request.data.get('contributors')
        if contributor_name is not None:
            try:
                if CustomUser.objects.filter(username=contributor_name).count == 1:
                    user = CustomUser.objects.get(username=contributor_name)
                else:
                    user = CustomUser.objects.get(id=contributor_name)
                Contributor.objects.get_or_create(user=user, project=instance)
            except CustomUser.DoesNotExist:
                return Response(
                    {"error": f"l'utilisateur {contributor_name} n'existe pas"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        contributor_id = request.data.get('contributors')
        if contributor_id is not None:
            try:
                contributor = Contributor.objects.get(
                    id=contributor_id)
                contributor.delete()
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            except Contributor.DoesNotExist:
                return Response(
                    {"error": f"le contributeur {contributor_id} "
                     + "n'existe pas dans ce projet"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return super().destroy(request, *args, **kwargs)


class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer

    def get_queryset(self):
        return Contributor.objects.filter(project_id=self.kwargs['project_pk'])


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IssuePermissions]

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs['project_pk'])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['project'] = self.kwargs['project_pk']
        return context


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [CommentPermissions]

    def get_queryset(self):
        return Comment.objects.filter(issue_id=self.kwargs['issue_pk'])
