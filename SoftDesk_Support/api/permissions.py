from rest_framework import permissions


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
        elif view.action in ['retrieve', 'list', 'update', 'partial_update']:
            return request.user.is_authenticated
        # Only allow admins to perform CRUD operations
        else:
            return request.user.is_staff

    # the object instance view
    def has_object_permission(self, request, view, obj):
        # Allow users to update or delete their own instance
        if view.action in ['update', 'partial_update', 'destroy']:
            result = obj == request.user or request.user.is_staff
            return result
        # Allow users to read their own instance
        elif view.action == 'retrieve':
            return request.user.is_authenticated
        # Only allow admins to perform CRUD operations
        else:
            return request.user.is_staff


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read-only
        if request.method in permissions.SAFE_METHODS:
            return True
        # Update and Delete
        return obj.author == request.user


class IsContributorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read-only
        if request.method in permissions.SAFE_METHODS:
            return True
        # Update and Delete
        return obj.author == request.user


class IsAssignedUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read-only
        if request.method in permissions.SAFE_METHODS:
            return True
        # Update and Delete
        return obj.author == request.user
