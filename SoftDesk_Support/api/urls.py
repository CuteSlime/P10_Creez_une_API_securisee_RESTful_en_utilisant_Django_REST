from django.urls import path

from .views import CustomUserAPIView


urlpatterns = [
    path('', CustomUserAPIView.as_view()),
]
