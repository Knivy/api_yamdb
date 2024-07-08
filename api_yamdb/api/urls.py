"""Адреса API."""

from django.urls import include, path  # type: ignore
from rest_framework import routers  # type: ignore
from .views import CategoryViewSet

app_name: str = 'api'

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')

v1_patterns: list[path] = [
    path('', include(router.urls)),
]

urlpatterns: list[path] = [
    path('v1/', include(v1_patterns)),
]