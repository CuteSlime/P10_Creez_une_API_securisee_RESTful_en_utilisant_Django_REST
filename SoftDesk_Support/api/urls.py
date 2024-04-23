from django.urls import path
from rest_framework_nested import routers

from .views import (
    CustomUserViewSet,
    ProjectViewSet,
    ContributorViewSet,
    IssueViewSet,
    CommentViewSet,
)
# router to the root for User and Project
router = routers.DefaultRouter()
router.register('users', CustomUserViewSet, basename="users")
router.register('projects', ProjectViewSet, basename="projects")

# nested router in project for Issue
projects_router = routers.NestedDefaultRouter(
    router, 'projects', lookup='project')
projects_router.register(
    'contributors', ContributorViewSet, basename="project-contributors")
projects_router.register('issues', IssueViewSet, basename="project-issues")

# nested router in issue for comment
issues_router = routers.NestedDefaultRouter(
    projects_router, 'issues', lookup='issue')
issues_router.register('comments', CommentViewSet, basename="issue-comments")

urlpatterns = router.urls + projects_router.urls + issues_router.urls
