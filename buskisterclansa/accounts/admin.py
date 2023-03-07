# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# This app
from .models import CustomUser
from .forms import CustomUserCreationForm

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Extra fields',
            {
                'fields': (
                    'is_admin',
                )
            }
        )
    )

admin.site.register(CustomUser, CustomUserAdmin)
