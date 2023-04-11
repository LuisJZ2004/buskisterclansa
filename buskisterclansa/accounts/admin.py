# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# This app
from .models import CustomUser
from .forms import CustomUserCreationForm

# Necessary to extra fields can be showed in the admin template
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
