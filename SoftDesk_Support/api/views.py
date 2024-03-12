from rest_framework import generics, permissions
from django.contrib.auth.models import Group

from accounts.models import CustomUser
from .serializers import UserSerializer, GroupSerializer


class CustomUserAPIView(generics.ListAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class GroupsAPIView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
