"""Контроллеры."""

from rest_framework import viewsets, filters, status  # type: ignore
from django.shortcuts import get_object_or_404  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from django_filters.rest_framework import DjangoFilterBackend  # type: ignore
from django.contrib.auth.tokens import default_token_generator  # type: ignore
from django.core.mail import send_mail  # type: ignore
from rest_framework.decorators import (  # type: ignore
    api_view, permission_classes)
from rest_framework.permissions import AllowAny  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework_simplejwt.tokens import AccessToken  # type: ignore
from django.conf import settings  # type: ignore
from django.http import JsonResponse  # type: ignore
from django.db import models  # type: ignore

from reviews.models import Category, Genre, Title, Review, Comment
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          ReviewSerializer, CommentSerializer)
from users.serializers import (UserGetOrCreationSerializer,
                               ConfirmationCodeSerializer)
from .permissions import (AdminOrReadListOnlyPermission,
                          AdminOrReadOnlyPermission, TextPermission)
from .filters import TitleFilter

User = get_user_model()


class PermissionsMixin(viewsets.ModelViewSet):
    """Миксин разрешений."""

    permission_classes = (AdminOrReadListOnlyPermission,)


class BaseTextViewSet(viewsets.ModelViewSet):
    """Миксин для текстов обзоров и комментариев."""

    permission_classes = (TextPermission,)
    ordering = ('-pub_date',)

    class Meta:
        abstract = True


class OrderingMixin(viewsets.ModelViewSet):
    """Миксин сортировки."""

    ordering = ('name',)

    class Meta:
        abstract = True


class CategoryViewSet(OrderingMixin, PermissionsMixin):
    """Обработка категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'  # Чтобы адрес был вида /categories/{slug}/


class GenreViewSet(OrderingMixin, PermissionsMixin):
    """Обработка жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(OrderingMixin):
    """Обработка произведений."""

    permission_classes = (AdminOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitleFilter
    http_method_names = ('get', 'post', 'patch', 'delete')
    ordering_fields = ('name', 'year', 'rating')

    def get_serializer_class(self):
        """Выбор сериализатора."""
        if self.action in {'list', 'retrieve'}:
            return TitleReadSerializer
        return TitleWriteSerializer
    
    def get_queryset(self):
        """Набор произведений."""
        if self.action in {'list', 'retrieve'}:
            return Title.objects.annotate(
                rating=models.Avg('reviews__score')
            )
        return Title.objects.all()


class ReviewViewSet(BaseTextViewSet):
    """Обработка обзоров."""

    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def perform_create(self, serializer):
        """Создание обзора."""
        serializer.save(author=self.request.user,
                        title=self.get_title())

    def get_title(self):
        """Получение произведения."""
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, id=title_id)

    def get_queryset(self):
        """Выбор обзоров."""
        return self.get_title().reviews.all()


class CommentViewSet(BaseTextViewSet):
    """Обработка комментариев."""

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        """Создание поста."""
        serializer.save(author=self.request.user,
                        review=self.get_review())

    def get_review(self):
        """Получение отзыва."""
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Review, id=review_id,
                                 title=title_id)

    def get_queryset(self):
        """Выбор комментариев."""
        return self.get_review().comments.all()


@api_view(('POST',))
@permission_classes((AllowAny,))
def send_confirmation_code(request):
    serializer = UserGetOrCreationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')

    user, created = User.objects.get_or_create(email=email,
                                               username=username)

    confirmation_code = default_token_generator.make_token(user)

    send_mail(
        'Код подтверждения',
        f'Ваш код подтверждения: {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False
    )

    return Response(serializer.validated_data)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt_token(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    token = AccessToken.for_user(user)
    return Response(
            {'token': str(token)}
        )


def page_not_found(request, exception) -> JsonResponse:
    """Ошибка 404: Объект не найден."""
    return JsonResponse({'message': 'Объект не найден.'},
                        status=status.HTTP_404_NOT_FOUND)
