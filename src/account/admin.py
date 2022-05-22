from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from django.contrib.auth.forms import UserChangeForm

from account.models import User


class UserForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"
        widgets = {"first_name": forms.TextInput, "last_name": forms.TextInput}


class UserAdmin(_UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    readonly_fields = ("date_joined",)
    form = UserForm
    ordering = ("-date_joined",)
    list_filter = ()


admin.site.register(User, UserAdmin)
