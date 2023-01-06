from django.test import TestCase
from django.forms import TextInput, PasswordInput, ClearableFileInput, FileInput
from app_users.forms import UserCreateForm, MyUserChangeForm, UserLoginForm, MyPasswordResetForm, MySetPasswordForm
from app_users.models import User


class UserCreateFormTest(TestCase):

    def test_field_password1_form(self):
        form = UserCreateForm()
        self.assertEqual(form.fields['password1'].max_length, 150)
        self.assertTrue(form.fields['password1'].required)
        self.assertEqual(form.fields['password1'].widget.attrs['maxlength'], '150')
        self.assertEqual(form.fields['password1'].widget.attrs['placeholder'], 'Введите пароль')
        self.assertEqual(form.fields['password1'].widget.__class__.__name__, PasswordInput().__class__.__name__)

    def test_field_password2_form(self):
        form = UserCreateForm()
        self.assertEqual(form.fields['password2'].max_length, 150)
        self.assertTrue(form.fields['password2'].required)
        self.assertEqual(form.fields['password2'].widget.attrs['maxlength'], '150')
        self.assertEqual(form.fields['password2'].widget.attrs['placeholder'], 'Введите пароль повторно')
        self.assertEqual(form.fields['password2'].widget.__class__.__name__, PasswordInput().__class__.__name__)

    def test_field_full_name_form(self):
        form = UserCreateForm()
        self.assertEqual(form.fields['full_name'].max_length, 254)
        self.assertTrue(form.fields['full_name'].required)
        self.assertEqual(form.fields['full_name'].widget.attrs['maxlength'], '254')
        self.assertEqual(form.fields['full_name'].widget.attrs['placeholder'], 'Введите ФИО')
        self.assertEqual(form.fields['full_name'].widget.__class__.__name__, TextInput().__class__.__name__)

    def test_field_email_form(self):
        form = UserCreateForm()
        self.assertEqual(form.fields['email'].max_length, 254)
        self.assertTrue(form.fields['email'].required)
        self.assertEqual(form.fields['email'].widget.attrs['maxlength'], '254')
        self.assertEqual(form.fields['email'].label, 'e-mail')
        self.assertEqual(form.fields['email'].widget.__class__.__name__, TextInput().__class__.__name__)

    def test_field_phoneNumber_form(self):
        form = UserCreateForm()
        self.assertTrue(form.fields['phoneNumber'].required)
        self.assertEqual(form.fields['phoneNumber'].widget.__class__.__name__, TextInput().__class__.__name__)

    def test_field_avatar_form(self):
        form = UserCreateForm()
        self.assertFalse(form.fields['avatar'].required)
        self.assertEqual(form.fields['avatar'].widget.attrs['accept'], ".jpg,.gif,.png")
        self.assertEqual(form.fields['avatar'].widget.__class__.__name__, ClearableFileInput().__class__.__name__)


class MyUserChangeFormTest(TestCase):

    def test_field_password1_form(self):
        form = MyUserChangeForm()
        self.assertEqual(form.fields['password1'].max_length, 150)
        self.assertTrue(form.fields['password1'].required)
        self.assertEqual(form.fields['password1'].widget.attrs['maxlength'], '150')
        self.assertEqual(form.fields['password1'].widget.attrs['placeholder'], 'Введите пароль')
        self.assertEqual(form.fields['password1'].widget.__class__.__name__, PasswordInput().__class__.__name__)

    def test_field_password2_form(self):
        form = MyUserChangeForm()
        self.assertEqual(form.fields['password2'].max_length, 150)
        self.assertTrue(form.fields['password2'].required)
        self.assertEqual(form.fields['password2'].widget.attrs['maxlength'], '150')
        self.assertEqual(form.fields['password2'].widget.attrs['placeholder'], 'Введите пароль повторно')
        self.assertEqual(form.fields['password2'].widget.__class__.__name__, PasswordInput().__class__.__name__)

    def test_field_full_name_form(self):
        form = MyUserChangeForm()
        self.assertEqual(form.fields['full_name'].max_length, 254)
        self.assertTrue(form.fields['full_name'].required)
        self.assertEqual(form.fields['full_name'].widget.attrs['maxlength'], '254')
        self.assertEqual(form.fields['full_name'].widget.attrs['placeholder'], 'Введите ФИО')
        self.assertEqual(form.fields['full_name'].widget.__class__.__name__, TextInput().__class__.__name__)

    def test_field_email_form(self):
        form = MyUserChangeForm()
        self.assertEqual(form.fields['email'].max_length, 254)
        self.assertTrue(form.fields['email'].required)
        self.assertEqual(form.fields['email'].widget.attrs['maxlength'], '254')
        self.assertEqual(form.fields['email'].label, 'e-mail')
        self.assertEqual(form.fields['email'].widget.__class__.__name__, TextInput().__class__.__name__)

    def test_field_phoneNumber_form(self):
        form = MyUserChangeForm()
        self.assertTrue(form.fields['phoneNumber'].required)
        self.assertEqual(form.fields['phoneNumber'].widget.__class__.__name__, TextInput().__class__.__name__)

    def test_field_avatar_form(self):
        form = MyUserChangeForm()
        self.assertFalse(form.fields['avatar'].required)
        self.assertEqual(form.fields['avatar'].widget.attrs['accept'], ".jpg,.gif,.png")
        self.assertEqual(form.fields['avatar'].widget.__class__.__name__, FileInput().__class__.__name__)


class UserLoginFormTest(TestCase):

    def test_field_password1_form(self):
        form = UserLoginForm()
        self.assertEqual(form.fields['username'].max_length, 254)
        self.assertEqual(form.fields['username'].label, 'Email')
        self.assertTrue(form.fields['username'].required)
        self.assertEqual(form.fields['username'].widget.attrs['maxlength'], 254)
        self.assertEqual(form.fields['username'].widget.attrs['placeholder'], 'Введите e-mail')
        self.assertEqual(form.fields['username'].widget.__class__.__name__, TextInput().__class__.__name__)

    def test_field_password_form(self):
        form = UserLoginForm()
        self.assertEqual(form.fields['password'].max_length, 150)
        self.assertEqual(form.fields['password'].label, 'Пароль')
        self.assertTrue(form.fields['password'].required)
        self.assertEqual(form.fields['password'].widget.attrs['maxlength'], '150')
        self.assertEqual(form.fields['password'].widget.attrs['placeholder'], 'Введите пароль')
        self.assertEqual(form.fields['password'].widget.__class__.__name__, PasswordInput().__class__.__name__)


class MyPasswordResetFormTest(TestCase):

    def test_field_password1_form(self):
        form = MyPasswordResetForm()
        self.assertEqual(form.fields['email'].max_length, 254)
        self.assertTrue(form.fields['email'].required)
        self.assertEqual(form.fields['email'].widget.attrs['maxlength'], '254')
        self.assertEqual(form.fields['email'].widget.__class__.__name__, TextInput().__class__.__name__)


class MySetPasswordFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(email='test@test.ru')
        user.set_password('12345')
        user.save()

    def test_field_password1_form(self):
        user = User.objects.get(email='test@test.ru')
        form = MySetPasswordForm(user)
        self.assertEqual(form.fields['new_password1'].max_length, 150)
        self.assertTrue(form.fields['new_password1'].required)
        self.assertEqual(form.fields['new_password1'].widget.attrs['maxlength'], '150')
        self.assertEqual(form.fields['new_password1'].widget.attrs['placeholder'], 'Введите пароль')
        self.assertEqual(form.fields['new_password1'].widget.__class__.__name__, PasswordInput().__class__.__name__)

    def test_field_password2_form(self):
        user = User.objects.get(email='test@test.ru')
        form = MySetPasswordForm(user)
        self.assertEqual(form.fields['new_password2'].max_length, 150)
        self.assertTrue(form.fields['new_password2'].required)
        self.assertEqual(form.fields['new_password2'].widget.attrs['maxlength'], '150')
        self.assertEqual(form.fields['new_password2'].widget.attrs['placeholder'], 'Введите пароль повторно')
        self.assertEqual(form.fields['new_password2'].widget.__class__.__name__, PasswordInput().__class__.__name__)
