from django import forms
from django.contrib import admin

from petition.models import Petition, PetitionNews


class PetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        fields = "__all__"
        widgets = {"title": forms.TextInput}


class PetitionAdmin(admin.ModelAdmin):
    model = Petition
    form = PetitionForm
    fields = (
        "title",
        "created_at",
        "description",
        "author",
        "signatories_count",
    )
    list_display = ("title", "author", "created_at", "signatories_count")
    readonly_fields = (
        "created_at",
        "signatories_count",
    )


admin.site.register(Petition, PetitionAdmin)
