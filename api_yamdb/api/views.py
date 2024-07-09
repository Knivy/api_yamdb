"""Контроллеры."""

from rest_framework import viewsets, generics, filters  # type: ignore
from rest_framework.pagination import LimitOffsetPagination  # type: ignore
from django.shortcuts import get_object_or_404  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from django.http import JsonResponse  # type: ignore
from django_filters.rest_framework import DjangoFilterBackend  # type: ignore

from reviews.models import Category, Genre, Title
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleReadSerializer, TitleWriteSerializer)
from .permissions import (AdminOrReadListOnlyPermission,
                          AdminOrReadOnlyPermission)

User = get_user_model()


class CategoryViewSet(viewsets.ModelViewSet):
    """Обработка категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadListOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'  # Чтобы адрес был вида /categories/{slug}/


class GenreViewSet(viewsets.ModelViewSet):
    """Обработка жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadListOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Обработка произведений."""

    queryset = Title.objects.all()
    permission_classes = (AdminOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year',
                        'genre__slug', 'category__slug')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer
