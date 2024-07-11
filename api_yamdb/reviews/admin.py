from django.contrib import admin  # type: ignore
from django.contrib.auth.admin import UserAdmin  # type: ignore

from users.models import YamdbUser

UserAdmin.fieldsets += (
    ('Extra Fields', {'fields': ('bio', 'role')}),
)
admin.site.register(YamdbUser, UserAdmin)
