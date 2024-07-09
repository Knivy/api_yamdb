from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CastomUser

UserAdmin.fieldsets += (
    ('Extra Fields', {'fields': ('bio', 'role')}),
)
admin.site.register(CastomUser, UserAdmin)
