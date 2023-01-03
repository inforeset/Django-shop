import re

from django.core.exceptions import ValidationError


class PasswordValidator(object):
    def validate(self, password, user=None):
        if not re.findall(r'^.*(?=.{8,})(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!#$%&?]).*$', password):
            raise ValidationError(
                "Пароль должен содержать 8 символов и минимум 1 цифру, одну букву, одну букву в верхнем регистре и один специальный символ из !#$%&?",
                code='password_invalid')

    def get_help_text(self):
        return "Пароль должен содержать 8 символов и минимум 1 цифру, одну букву, одну букву в верхнем регистре и один специальный символ из !#$%&?"
