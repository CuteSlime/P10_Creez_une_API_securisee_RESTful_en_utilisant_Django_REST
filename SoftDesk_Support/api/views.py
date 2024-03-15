from rest_framework import viewsets, permissions
from django.contrib.auth.models import Group

from accounts.models import CustomUser
from .serializers import UserSerializer, GroupSerializer
from .permissions import CustomUserPermissions


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
