"""Адреса проекта."""

from django.contrib import admin  # type: ignore
from django.urls import include, path  # type: ignore
from django.views.generic import TemplateView  # type: ignore

urlpatterns: list[path] = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
