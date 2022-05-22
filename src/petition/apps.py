from django.apps import AppConfig


class PetitionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "petition"
    verbose_name = "Petitions"

    def ready(self):
        from . import signals  # noqa
