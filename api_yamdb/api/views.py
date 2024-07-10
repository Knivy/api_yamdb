"""Контроллеры."""

from datetime import datetime as dt

from rest_framework import viewsets, filters  # type: ignore
from django.shortcuts import get_object_or_404  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from django_filters.rest_framework import DjangoFilterBackend  # type: ignore

from reviews.models import Category, Genre, Title, Review, Comment
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          ReviewSerializer, CommentSerializer)
from .permissions import (AdminOrReadListOnlyPermission,
                          AdminOrReadOnlyPermission, TextPermission)

User = get_user_model()


class PermissionsMixin(viewsets.ModelViewSet):
    """Миксин разрешений."""

    # permission_classes = (AdminOrReadListOnlyPermission,)


class TextPermissionsMixin(viewsets.ModelViewSet):
    """Миксин разрешений."""

    # permission_classes = (TextPermission,)


class CategoryViewSet(PermissionsMixin, viewsets.ModelViewSet):
    """Обработка категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'  # Чтобы адрес был вида /categories/{slug}/


class GenreViewSet(PermissionsMixin, viewsets.ModelViewSet):
    """Обработка жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
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


class ReviewViewSet(TextPermissionsMixin, viewsets.ModelViewSet):
    """Обработка обзоров."""

    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def perform_create(self, serializer):
        """Создание поста."""
        serializer.save(author=self.request.user,
                        title=self.get_title(),
                        pub_date=dt.now().strftime('%Y-%m-%dT%H:%M:%SZ'))

    def get_title(self):
        """Получение произведения."""
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, id=title_id)

    def get_queryset(self):
        """Выбор обзоров."""
        return self.get_title().reviews.all()


class CommentViewSet(TextPermissionsMixin, viewsets.ModelViewSet):
    """Обработка комментариев."""

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        """Создание поста."""
        serializer.save(author=self.request.user,
                        review=self.get_review(),
                        pub_date=dt.now().strftime('%Y-%m-%dT%H:%M:%SZ'))

    def get_review(self):
        """Получение отзыва."""
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, id=review_id)

    def get_queryset(self):
        """Выбор комментариев."""
        return self.get_review().comments.all()
