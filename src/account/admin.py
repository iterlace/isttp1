from django import forms
from django.contrib import admin

from account.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"
        widgets = {"first_name": forms.TextInput, "last_name": forms.TextInput}


class UserAdmin(admin.ModelAdmin):
    fields = (
        "first_name",
        "last_name",
        "email",
        "date_joined",
        "is_staff",
        "is_superuser",
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    readonly_fields = ("date_joined",)
    form = UserForm


admin.site.register(User, UserAdmin)
