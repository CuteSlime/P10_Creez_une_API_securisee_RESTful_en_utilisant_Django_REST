from rest_framework import viewsets, permissions
from django.contrib.auth.models import Group

from accounts.models import CustomUser
from .serializers import UserSerializer, GroupSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class GroupsViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
