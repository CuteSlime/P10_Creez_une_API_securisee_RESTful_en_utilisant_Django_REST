from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import CustomUserViewSet

router = SimpleRouter()
router.register('users', CustomUserViewSet, basename="users"),
urlpatterns = router.urls
