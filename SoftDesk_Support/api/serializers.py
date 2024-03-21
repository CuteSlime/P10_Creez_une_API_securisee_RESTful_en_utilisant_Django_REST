from django.contrib.auth.models import Group
from rest_framework import serializers

from accounts.models import CustomUser
from Project.models import Project, Contributor


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
            'created_time',
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

        if age < 16:
            raise serializers.ValidationError(
                "les Utilisateur de moin de 16 ans ne sont pas accepter")

        return data


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class ContributorSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Contributor
        fields = ['user', 'created_time']


class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    contributors = ContributorSerializer(many=True, read_only=True)
    type = serializers.ChoiceField(choices=Project.TYPE_CHOICES)

    class Meta:
        model = Project
        fields = [
            'id',
            'author',
            'contributors',
            'name',
            'description',
            'type',
            'created_time',
        ]

    def validate(self, data):
        contributor_id = data.get('contributor', None)

        if contributor_id is not None:
            try:
                CustomUser.objects.get(id=contributor_id)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError(
                    "l'id {} ne correspond à aucun utilisateurs connu".format(contributor_id))

        return data

    def update(self, instance, validated_data):
        contributor_id = validated_data.pop('contributor', None)
        instance = super().update(instance, validated_data)

        if contributor_id is not None:
            user = CustomUser.objects.get(id=contributor_id)
            Contributor.objects.get_or_create(user=user, project=instance)

        return instance
