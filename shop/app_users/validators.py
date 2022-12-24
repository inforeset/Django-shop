import re

from django.core.exceptions import ValidationError


class PasswordValidator(object):
    def validate(self, password, user=None):
        if not re.findall(r'^.*(?=.{8,})(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!#$%&?]).*$', password):
            raise ValidationError(
                "Password must contain 8 characters and at least one number, one letter, one letter in Upper case and one unique character such as !#$%&?",
                code='password_invalid')

    def get_help_text(self):
        return "Password must contain 8 characters and at least one number, one letter, one letter in Upper case and one unique character such as !#$%&?"
