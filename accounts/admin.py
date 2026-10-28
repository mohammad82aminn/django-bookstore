from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ("username", "email", "age", "is_staff")

    fieldsets = [
        *(UserAdmin.fieldsets or ()),
        ("Additional information", {"fields": ("age",)}),
    ]

    add_fieldsets = (
        (None, {"fields": ("username", "age", "password1", "password2")}),
    )


admin.site.register(CustomUser, CustomUserAdmin)