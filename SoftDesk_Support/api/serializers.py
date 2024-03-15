from django.contrib.auth.models import Group
from accounts.models import CustomUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'age',
            'groups',
            'can_be_contacted',
            'can_data_be_shared',
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if instance.can_data_be_shared or request.user == instance or request.user.is_staff:
            representation['age'] = instance.age
            representation['email'] = instance.email
        else:
            representation.pop('age', None)
            representation.pop('email', None)
        return representation


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']
