from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import CustomUserViewSet, ProjectViewSet, ContributorViewSet

router = SimpleRouter()
router.register('users', CustomUserViewSet, basename="users"),
router.register('projects', ProjectViewSet, basename="projects"),
router.register('contributors', ContributorViewSet, basename="contributors"),
urlpatterns = router.urls
