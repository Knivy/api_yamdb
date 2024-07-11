"""Адреса API."""

from django.urls import include, path  # type: ignore
from rest_framework import routers  # type: ignore
from .views import (CategoryViewSet, GenreViewSet,
                    ReviewViewSet, CommentViewSet, TitleViewSet,
                    get_jwt_token, send_confirmation_code)
from users.views import UserViewSet

app_name: str = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('users', UserViewSet, basename='users')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                   basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
router_v1.register('titles', TitleViewSet, basename='titles')

v1_auth_patterns = [
    path('signup/', send_confirmation_code, name='send_confirmation_code'),
    path('token/', get_jwt_token, name='get_token'),
]

v1_patterns: list[path] = [
    path('auth/', include(v1_auth_patterns)),
    path('', include(router_v1.urls)),
]

urlpatterns: list[path] = [
    path('v1/', include(v1_patterns)),
]
handler404 = 'api.views.page_not_found'
