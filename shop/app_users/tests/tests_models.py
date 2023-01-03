import tempfile
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from app_users.models import User


class UserTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(email='test@test.ru')
        user.set_password('12345')
        user.save()

    def test_email_label(self):
        user = User.objects.get(email='test@test.ru')
        field_label = user._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'Email адрес')

    def test_email_unique(self):
        user = User.objects.get(email='test@test.ru')
        unique = user._meta.get_field('email').unique
        self.assertTrue(unique)

    def test_full_name_label(self):
        user = User.objects.get(email='test@test.ru')
        field_label = user._meta.get_field('full_name').verbose_name
        self.assertEqual(field_label, 'Полное имя')

    def test_full_name_max_length(self):
        user = User.objects.get(email='test@test.ru')
        max_length = user._meta.get_field('full_name').max_length
        self.assertEqual(max_length, 254)

    def test_date_joined_label(self):
        user = User.objects.get(email='test@test.ru')
        field_label = user._meta.get_field('date_joined').verbose_name
        self.assertEqual(field_label, 'Дата регистрации')

    def test_is_active_label(self):
        user = User.objects.get(email='test@test.ru')
        field_label = user._meta.get_field('is_active').verbose_name
        self.assertEqual(field_label, 'Активен')

    def test_avatar_label(self):
        user = User.objects.get(email='test@test.ru')
        field_label = user._meta.get_field('avatar').verbose_name
        self.assertEqual(field_label, 'Аватар')

    def test_phoneNumber_label(self):
        user = User.objects.get(email='test@test.ru')
        field_label = user._meta.get_field('phoneNumber').verbose_name
        self.assertEqual(field_label, 'Телефон')

    def test_phoneNumber_max_length(self):
        user = User.objects.get(email='test@test.ru')
        max_length = user._meta.get_field('phoneNumber').max_length
        self.assertEqual(max_length, 10)

    def test_phoneNumber_unique(self):
        user = User.objects.get(email='test@test.ru')
        unique = user._meta.get_field('phoneNumber').unique
        self.assertTrue(unique)

    def test_is_staff_label(self):
        user = User.objects.get(email='test@test.ru')
        field_label = user._meta.get_field('is_staff').verbose_name
        self.assertEqual(field_label, 'Сотрудник')

    def test_avatar_validator_extension(self):
        image = SimpleUploadedFile(tempfile.NamedTemporaryFile(suffix=".webp").name, b"file_content",
                                   content_type="image/webp")
        user = User.objects.create(email='test2@test.ru', avatar=image, phoneNumber=1234567890,
                                   full_name='test_fulname')
        user.set_password('12345')
        user.save()
        with self.assertRaises(ValidationError,
                               msg='Расширение не поддерживается. Разрешенные расширения .jpg .gif .png'):
            user.full_clean()

    def test_phoneNumber_validator_extension(self):
        user = User.objects.create(email='test2@test.ru', phoneNumber=123456789, full_name='test_fulname')
        user.set_password('12345')
        user.save()
        with self.assertRaises(ValidationError):
            user.full_clean()
