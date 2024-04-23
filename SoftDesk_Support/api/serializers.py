from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from accounts.models import CustomUser
from project.models import Project, Contributor
from issue.models import Issue, Comment


class CustomSlugRelatedField(serializers.SlugRelatedField):
    """
        CustomSlug relatedField that return a list of available user with the error
    """

    def to_internal_value(self, data):
        try:
            value = self.get_queryset().get(**{self.slug_field: data})
            return value
        except ObjectDoesNotExist:
            available_users = self.get_queryset().values_list('id', 'username')
            user_list = ', '.join(
                [f'{username} (ID: {id})' for id, username in available_users])

            raise serializers.ValidationError(
                f"L'utilisateur {
                    data} n'existe pas. Les choix disponible sont : {user_list}"
            )


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
    """
    Serializer for the CustomUser model.

    Fields:
    - id: The ID of the user.
    - username: The username of the user.
    - password: The password of the user (write-only).
    - email: The email of the user. (hide if can_data_be_shared is false)
    - age: The age of the user. (hide if can_data_be_shared is false)
    - can_be_contacted: A boolean indicating whether the user can be contacted.
    - can_data_be_shared: A boolean indicating whether the user's data can be shared.
    - created_time: The time the user was created.

    Validation:
    - validate: Ensures the user's age is not less than 16.
    """
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'password',
            'email',
            'age',
            'can_be_contacted',
            'can_data_be_shared',
            'created_time',
        ]
        extra_kwargs = {'password': {'write_only': True}}

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
        age = data.get('age')

        if age is not None and age < 16:
            raise serializers.ValidationError(
                "les Utilisateur de moin de 16 ans ne sont pas accepter")

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class ContributorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contributor model.

    Fields:
    - id: The ID of the contributor.
    - user: The user who is the contributor.
    - project: The project the user is contributing to.
    - created_time: The time the contributor was created.

    Validation:
    - create: Ensures the project exist in the view and set it.
    """

    user = serializers.StringRelatedField()
    project = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'created_time']

    def create(self, validated_data):
        # Get the current  project, then set it.
        validated_data['project'] = Project.objects.get(
            pk=self.context['view'].kwargs['project_pk'])
        return super().create(validated_data)


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Project model.

    Fields:
    - id: The ID of the project.
    - author: The author of the project.
    - contributors: The list of contributors of the project.
    - name: The name of the project.
    - description: The description of the project.
    - type: The type of the project.
    - created_time: The time the project was created.

    Validation:
    - create: use the authenticated user to set the author.
    """

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
        if self.context.get('detail_view'):
            representation['contributors'] = ContributorSerializer(
                instance.contributor_set.all(), many=True).data
        else:
            representation.pop('contributors', None)
        return representation

    def create(self, validated_data):
        # Get the current authenticated user and set it as author.
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class IssueSerializer(serializers.ModelSerializer):
    """
    Serializer for the Issue model.

    Fields:
    - id: The ID of the issue.
    - author: The author of the issue.
    - assign_to: The user assigned to the issue.
    - project: The project the issue belongs to.
    - title: The title of the issue.
    - description: The description of the issue.
    - statue: The status of the issue.
    - priority: The priority of the issue.
    - tag: The tag of the issue.
    - created_time: The time the issue was created.

    Validation:
    - create: use the authenticate user and get the project from the view 
    to set the author and project of the issue
    """

    author = serializers.StringRelatedField()
    assign_to = CustomSlugRelatedField(
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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not self.context.get('detail_view'):
            representation.pop('project', None)
        return representation

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
    """
    Serializer for the Comment model.

    Fields:
    - id: The ID of the comment.
    - author: The author of the comment.
    - issue: The issue the comment belongs to.
    - description: The description of the comment.
    - uuid: The UUID of the comment.
    - created_time: The time the comment was created.

    Validation:
    - create: use the authenticate user and get the project from the view 
    to set the author and project of the comment
    """

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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not self.context.get('detail_view'):
            representation.pop('issue', None)
            representation.pop('uuid', None)
        return representation

    def create(self, validated_data):
        # Get the current authenticated user and issue, then set them to their respective field.
        validated_data['author'] = self.context['request'].user
        validated_data['issue'] = Issue.objects.get(
            pk=self.context['view'].kwargs['issue_pk'])
        return super().create(validated_data)
