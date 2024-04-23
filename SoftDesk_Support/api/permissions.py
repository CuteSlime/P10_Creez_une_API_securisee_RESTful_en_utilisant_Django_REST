from rest_framework import permissions
from project.models import Project
from issue.models import Issue


class CustomUserPermissions(permissions.BasePermission):
    """
    CustomUser model permissions for admin, authenticated users and guests.
    """

    # the list view
    def has_permission(self, request, view):

        # Allow OPTIONS requests
        if request.method == 'OPTIONS':
            return True

        # Allow guest users to create a new user
        if view.action == 'create':
            return True

        # allow authenticated users to Read the user list
        # and give other permissions that are needed for the object permission
        elif view.action in ['retrieve', 'list', 'update', 'partial_update', 'destroy']:
            return request.user.is_authenticated

        # Only allow admins to perform CRUD operations
        else:
            return request.user.is_staff

    # the object instance view
    def has_object_permission(self, request, view, obj):

        # Allow OPTIONS requests
        if request.method == 'OPTIONS':
            return True

        # Allow users to update or delete their own instance
        if view.action in ['update', 'partial_update', 'destroy']:
            return obj == request.user or request.user.is_staff

        # Allow users to read their own instance
        elif view.action == 'retrieve':
            return request.user.is_authenticated

        # Only allow admins to perform CRUD operations
        else:
            return request.user.is_staff


class ProjectPermissions(permissions.BasePermission):
    """
    Custom permissions for Project
    """

    def has_permission(self, request, view):

        # Allow OPTIONS requests
        if request.method == 'OPTIONS':
            return True

        # Allow any authenticated user to create a new project
        if view.action == 'create':
            return request.user.is_authenticated

        # allow authenticated users to Read the project list
        # and give other permissions that are needed for the object permission
        elif view.action in ['retrieve', 'list', 'update', 'partial_update', 'destroy']:
            return request.user.is_authenticated

        # Only allow admins to perform CRUD operations
        else:
            return request.user.is_staff

    def has_object_permission(self, request, view, obj):

        # Allow OPTIONS requests
        if request.method == 'OPTIONS':
            return True

        # Check if the user is a contributor of the project
        is_contributor = obj.contributors.filter(
            id=request.user.id).exists()

        # Allow the author of the project to delete the project
        if view.action == 'destroy':
            return obj.author == request.user or request.user.is_staff

        # Allow the author of the project to update certain attributes
        elif view.action in ['update', 'partial_update']:
            if obj.author == request.user or request.user.is_staff:
                # Check if the attribute being updated is allowed
                allowed_attributes = ['contributors',
                                      'name', 'description', 'type']
                return all(attribute in allowed_attributes for attribute in request.data.keys())

        # Allow contributors and the author of the project to read the project
        elif view.action == 'retrieve':
            return is_contributor or obj.author == request.user or request.user.is_staff

        return False


class IssuePermissions(permissions.BasePermission):
    """
    Custom permissions for Issue
    """

    def has_permission(self, request, view):
        # Allow OPTIONS requests
        if request.method == 'OPTIONS':
            return True

        # get the project and look if user is a contributor
        project_id = view.kwargs.get('project_pk')
        if project_id is not None:
            project = Project.objects.get(id=project_id)
            is_contributor = project.contributors.filter(
                id=request.user.id).exists()

        # Only allow authenticated users who are contributors to the project to create a new issue
        if view.action == 'create':
            return is_contributor or request.user.is_staff

        # allow project contributor to Read the issue list
        # and give other permissions that are needed for the object permission
        elif view.action in ['retrieve', 'list', 'update', 'partial_update', 'destroy']:
            return is_contributor or request.user.is_staff

        # Only allow admins to perform CRUD operations
        else:
            return request.user.is_staff

    def has_object_permission(self, request, view, obj):

        # Allow OPTIONS requests
        if request.method == 'OPTIONS':
            return True

        # Check if the user is a contributor of the project
        is_contributor = obj.project.contributors.filter(
            id=request.user.id).exists()

        # Allow the author of the issue to delete the issue
        if view.action == 'destroy':
            return obj.author == request.user or request.user.is_staff

        # Allow the author of the issue to update certain attributes
        elif view.action in ['update', 'partial_update']:
            if obj.author == request.user or request.user.is_staff:
                # Check if the attribute being updated is allowed
                allowed_attributes = ['assign_to', 'title',
                                      'description', 'statue', 'priority', 'tag']
                return all(attribute in allowed_attributes for attribute in request.data.keys())

            elif obj.assign_to == request.user:
                # Check if the attribute being updated is 'statue'
                return all(attribute == 'statue' for attribute in request.data.keys())

        # Allow contributors and the author of the issue to read the issue
        elif view.action == 'retrieve':
            return is_contributor or obj.author == request.user or request.user.is_staff

        return False


class CommentPermissions(permissions.BasePermission):
    """
    Custom permissions for comment
    """

    def has_permission(self, request, view):

        # Allow OPTIONS requests
        if request.method == 'OPTIONS':
            return True

        # get the project and look if user is a contributor
        project_id = view.kwargs.get('project_pk')
        if project_id is not None:
            project = Project.objects.get(id=project_id)
            is_contributor = project.contributors.filter(
                id=request.user.id).exists()

        # Only allow authenticated users who are contributors to the project to create a new comment
        if view.action == 'create':
            return is_contributor or request.user.is_staff

        # allow project contributor to Read the comment list
        # and give other permissions that are needed for the object permission
        elif view.action in ['retrieve', 'list', 'update', 'partial_update', 'destroy']:
            return is_contributor or request.user.is_staff

        # Only allow admins to perform CRUD operations
        else:
            return request.user.is_staff

    def has_object_permission(self, request, view, obj):

        # Allow OPTIONS requests
        if request.method == 'OPTIONS':
            return True

        # Check if the user is a contributor of the project
        is_contributor = obj.issue.project.contributors.filter(
            id=request.user.id).exists()

        # Allow the author of the comment to delete the comment
        if view.action == 'destroy':
            return obj.author == request.user

        # Allow the author of the comment to update certain attributes
        elif view.action in ['update', 'partial_update']:
            if obj.author == request.user:
                # Check if the attribute being updated is allowed
                allowed_attributes = ['description']
                return all(attribute in allowed_attributes for attribute in request.data.keys())

        # Allow contributors and the author of the comment to read the comment
        elif view.action == 'retrieve':
            return is_contributor or obj.author == request.user

        return False
