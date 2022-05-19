from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text="E-Mail")
    first_name = forms.CharField(max_length=64, help_text="First Name")
    last_name = forms.CharField(max_length=64, help_text="Last Name")

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )
