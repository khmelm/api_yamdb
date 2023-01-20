from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Дополнительная информация',
            {
                'fields': (
                    'bio',
                    'role',
                ),
            },
        ),
    )
    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email',),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
