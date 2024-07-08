"""Контроллеры."""

from rest_framework import viewsets, generics, filters  # type: ignore
from rest_framework.pagination import LimitOffsetPagination  # type: ignore
from django.shortcuts import get_object_or_404  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from django.http import JsonResponse  # type: ignore

from reviews.models import Category
from .serializers import (CategorySerializer,)
from .permissions import AdminOrReadOnlyPermission

User = get_user_model()


class CategoryViewSet(viewsets.ModelViewSet):
    """Обработка категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
