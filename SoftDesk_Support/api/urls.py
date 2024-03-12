from django.urls import path

from .views import CustomUserAPIView


urlpatterns = [
    path('user/', CustomUserAPIView.as_view()),
]
