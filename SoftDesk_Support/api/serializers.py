from django.contrib.auth.models import Group
from rest_framework import serializers

from accounts.models import CustomUser
from project.models import Project, Contributor
from issue.models import Issue, Comment


class ChoiceFieldWithCustomErrorMessage(serializers.ChoiceField):
    """ error message that give the list of available choices."""

    def run_validation(self, data=serializers.empty):
        try:
            return super().run_validation(data)
        except serializers.ValidationError:
            choices = ', '.join(self.choices.keys())
            raise serializers.ValidationError(
                f" '{data}' n'est pas un choix valide. Les choix disponible sont : {choices}")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'age',
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
    project = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Contributor
        fields = ['user', 'project', 'created_time']

    def create(self, validated_data):
        # Get the current  project, then set it.
        validated_data['project'] = Project.objects.get(
            pk=self.context['view'].kwargs['project_pk'])
        return super().create(validated_data)


class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    contributors = ContributorSerializer(many=True, read_only=True)
    type = ChoiceFieldWithCustomErrorMessage(choices=Project.TYPE_CHOICES)

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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['contributors'] = ContributorSerializer(
            instance.contributor_set.all(), many=True).data
        return representation

    def create(self, validated_data):
        # Get the current authenticated user and set it as author.
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class IssueSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    assign_to = serializers.SlugRelatedField(
        queryset=CustomUser.objects.none(),
        slug_field='username',
        required=False,
        allow_null=True,
    )
    project = serializers.SlugRelatedField(slug_field='name', read_only=True)
    statue = ChoiceFieldWithCustomErrorMessage(choices=Issue.STATUE_CHOICES)
    priority = ChoiceFieldWithCustomErrorMessage(
        choices=Issue.PRIORITY_CHOICES)
    tag = ChoiceFieldWithCustomErrorMessage(choices=Issue.TAG_CHOICES)

    class Meta:
        model = Issue
        fields = [
            'id',
            'author',
            'assign_to',
            'project',
            'title',
            'description',
            'statue',
            'priority',
            'tag',
            'created_time',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'context' in kwargs:
            project_id = kwargs['context'].get('project')
            self.fields['assign_to'].queryset = CustomUser.objects.filter(
                id__in=Contributor.objects.filter(
                    project=project_id).values_list('user', flat=True)
            )

    def create(self, validated_data):
        # Get the current authenticated user and project, then set them to their respective field.
        validated_data['author'] = self.context['request'].user
        validated_data['project'] = Project.objects.get(
            pk=self.context['view'].kwargs['project_pk'])
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    issue = serializers.SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'author',
            'issue',
            'description',
            'uuid',
            'created_time',
        ]

    def create(self, validated_data):
        # Get the current authenticated user and issue, then set them to their respective field.
        validated_data['author'] = self.context['request'].user
        validated_data['issue'] = Issue.objects.get(
            pk=self.context['view'].kwargs['issue_pk'])
        return super().create(validated_data)
