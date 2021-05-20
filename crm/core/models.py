from typing import Optional
from django.db import models

# Create your models here.
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from django.http.request import HttpRequest
# Unregister the provided model admin
admin.site.unregister(User)

# Register out own model admin, based on the default UserAdmin


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    readonly_fields = [
        'date_joined',
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        disabled_fields = set()  # type: Set[str]

        if not is_superuser:
            disabled_fields |= {
                'username',
                'is_superuser',
                'user_permissions'
            }
        # Prevent non-superusers from editing their own permissions
        if (
            not is_superuser
            and obj is not None
            and obj == request.user
        ):
            disabled_fields |= {
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            }
        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    # def has_module_permission(self, request) -> bool:
    #     return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False
