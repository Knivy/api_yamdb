from django.contrib import admin  # type: ignore
from django.contrib.auth.models import Group  # type: ignore

from .models import Category, Comment, Genre, Review, Title


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.unregister(Group)
