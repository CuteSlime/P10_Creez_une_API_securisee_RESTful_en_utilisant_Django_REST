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

    def validate(self, data):
        age = data.get('age', 0)
        # can_be_contacted = data.get('can_be_contacted', False)
        # can_data_be_shared = data.get('can_data_be_shared', False)

        if age < 16:
            raise serializers.ValidationError(
                "les Utilisateur de moin de 16 ans ne sont pas accepter")

        return data


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']
