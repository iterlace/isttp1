from django.core.exceptions import ValidationError


class NumericPasswordValidator:
    """
    Validate whether the password is alphanumeric.
    """

    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                "Your password must contain at least one letter or a special symbol.",
                code="password_entirely_numeric",
            )

    def get_help_text(self):
        return "Your password can’t be entirely numeric."
