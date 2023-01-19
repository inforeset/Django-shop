from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, FileExtensionValidator
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    image_validator = FileExtensionValidator(
        allowed_extensions=['png', 'jpg', 'gif'],
        message='Расширение не поддерживается. Разрешенные расширения .jpg .gif .png'
    )

    def validate_image_size(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 2.0
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError("Максимальный размер файла %sMB" % str(megabyte_limit), code='invalid')

    email = models.EmailField(unique=True, verbose_name='Email адрес')
    full_name = models.CharField(max_length=254, verbose_name='Полное имя')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name='Аватар',
                               validators=[validate_image_size, image_validator])
    phoneNumberRegex = RegexValidator(regex=r"^\d{10}$")
    phoneNumber = models.CharField(validators=[phoneNumberRegex], max_length=10, unique=True, verbose_name='Телефон')
    is_staff = models.BooleanField(default=False, verbose_name='Сотрудник')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class ProxyGroups(Group):
    class Meta:
        proxy = True
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
