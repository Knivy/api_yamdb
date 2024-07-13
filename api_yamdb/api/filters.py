"""Фильтры."""

from django_filters import rest_framework as filters  # type: ignore

from reviews.models import Title


class TitleFilter(filters.FilterSet):
    # Нечувствительно к регистру
    genre = filters.CharFilter(field_name='genre__slug',
                               lookup_expr='iexact')
    category = filters.CharFilter(field_name='category__slug',
                                  lookup_expr='iexact')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ('year',)
