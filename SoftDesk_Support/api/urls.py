from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import (
    CustomUserViewSet,
    ProjectViewSet,
    ContributorViewSet,
    IssueViewSet,
    CommentViewSet,
)
router = SimpleRouter()
router.register('users', CustomUserViewSet, basename="users"),
router.register('contributors', ContributorViewSet, basename="contributors"),
router.register('projects', ProjectViewSet, basename="projects"),
router.register('issues', IssueViewSet, basename="issues"),
router.register('comments', CommentViewSet, basename="comments"),

urlpatterns = router.urls
