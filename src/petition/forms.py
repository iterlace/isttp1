from django import forms

from .models import Petition


class PetitionCreateForm(forms.ModelForm):
    title = forms.CharField(max_length=200, help_text="Petition title")
    description = forms.CharField(
        max_length=2400,
        widget=forms.Textarea(),
        help_text="Describe the petition",
    )

    class Meta:
        model = Petition
        fields = (
            "title",
            "description",
        )
