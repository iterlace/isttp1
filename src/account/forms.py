import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import User

alphabetic_re = re.compile(r"^[a-zа-яєїіґ\s]*$", flags=re.I)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text="E-Mail")
    first_name = forms.CharField(max_length=64, help_text="First Name")
    last_name = forms.CharField(max_length=64, help_text="Last Name")

    def clean_first_name(self):
        data = self.cleaned_data["first_name"].strip()
        if not alphabetic_re.match(data):
            raise ValidationError(
                "Your first name contains prohibited characters", code="invalid"
            )
        return data.title()

    def clean_last_name(self):
        data = self.cleaned_data["last_name"].strip()
        if not alphabetic_re.match(data):
            raise ValidationError(
                "Your last name contains prohibited characters", code="invalid"
            )
        return data.title()

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )
