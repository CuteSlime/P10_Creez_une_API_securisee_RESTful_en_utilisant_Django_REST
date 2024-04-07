from rest_framework import permissions
from project.models import Project
from issue.models import Issue


class CustomUserPermissions(permissions.BasePermission):
    """
    Custom user permissions for admin, authenticated users and guests.
    """

    # the list view
    def has_permission(self, request, view):
        # Allow guest users to create a new user
        if view.action == 'create':
            return True
        # Only allow authenticated users to read the users list
        elif view.action in ['retrieve', 'list', 'update', 'partial_update', 'destroy']:
            return request.user.is_authenticated
        # Only allow admins to perform CRUD operations
        else:
            return request.user.is_staff

    # the object instance view
    def has_object_permission(self, request, view, obj):
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
        # Allow any authenticated user to create a new project
        if view.action == 'create':
            return request.user.is_authenticated
        # Only allow authenticated users to read the projects list
        elif view.action in ['retrieve', 'list', 'update', 'partial_update', 'destroy']:
            return request.user.is_authenticated
        # Only allow admins to perform CRUD operations
        else:
            return request.user.is_staff

    def has_object_permission(self, request, view, obj):
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
        project_id = view.kwargs.get('project_pk')
        if project_id is not None:
            project = Project.objects.get(id=project_id)
            is_contributor = project.contributors.filter(
                id=request.user.id).exists()
        # Only allow authenticated users who are contributors to the project to create a new issue
        if view.action == 'create':
            return is_contributor or request.user.is_staff
        # Only allow authenticated users to read the issues list
        elif view.action in ['retrieve', 'list', 'update', 'partial_update', 'destroy']:
            return is_contributor or request.user.is_staff
        # Only allow admins to perform CRUD operations
        else:
            return request.user.is_staff

    def has_object_permission(self, request, view, obj):
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
    Custom permissions for Issue
    """

    def has_permission(self, request, view):
        project_id = view.kwargs.get('project_pk')
        if project_id is not None:
            project = Project.objects.get(id=project_id)
            is_contributor = project.contributors.filter(
                id=request.user.id).exists()
        # Only allow authenticated users who are contributors to the project to create a new issue
        if view.action == 'create':
            return is_contributor or request.user.is_staff
        # Only allow authenticated users to read the issues list
        elif view.action in ['retrieve', 'list', 'update', 'partial_update', 'destroy']:
            return is_contributor or request.user.is_staff
        # Only allow admins to perform CRUD operations
        else:
            return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # Check if the user is a contributor of the project
        is_contributor = obj.issue.project.contributors.filter(
            id=request.user.id).exists()

        # Allow the author of the issue to delete the issue
        if view.action == 'destroy':
            return obj.author == request.user
        # Allow the author of the issue to update certain attributes
        elif view.action in ['update', 'partial_update']:
            if obj.author == request.user:
                # Check if the attribute being updated is allowed
                allowed_attributes = ['description']
                return all(attribute in allowed_attributes for attribute in request.data.keys())
        # Allow contributors and the author of the issue to read the issue
        elif view.action == 'retrieve':
            return is_contributor or obj.author == request.user

        return False
