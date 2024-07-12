"""Контроллеры."""

from rest_framework import filters, status  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from rest_framework.decorators import action  # type: ignore
from rest_framework.viewsets import ModelViewSet  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore

from .serializers import UserSerializer, SingleUserSerializer
from .permissions import AdminOnlyPermission

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnlyPermission,)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)

    @action(
        detail=False,
        methods=('get', 'patch'),
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'me':
            return SingleUserSerializer
        return super().get_serializer_class()
