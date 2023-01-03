from django.test import TestCase
from django.urls import reverse
from app_users.models import User


class MyRegistrationTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(email='test@test.ru')
        user.set_password('12345')
        user.save()

    def test_registration_page_exist_at_desired_location(self):
        response = self.client.get(reverse('registration'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Зарегистрироваться')

    def test_registration_page_used_right_template(self):
        response = self.client.get(reverse('registration'))
        self.assertTemplateUsed(response, 'app_users/registration.html')

    def test_registration_page_redirect_if_loged(self):
        self.client.login(email='test@test.ru', password='12345')
        response = self.client.get(reverse('registration'))
        self.assertRedirects(response=response, expected_url=reverse('profile'), status_code=302,
                             target_status_code=200)

    def test_registration_page_post(self):
        response = self.client.post(reverse('registration'),
                                    {'password1': 'Wqdsfsgsg1421!', 'password2': 'Wqdsfsgsg1421!',
                                     'full_name': 'test_user', 'email': 'test2@test.ru',
                                     'phoneNumber': '1234567890'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='test2@test.ru').exists())


class ProfileViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(email='test@test.ru')
        user.set_password('12345')
        user.save()

    def test_profile_page_exist_at_desired_location(self):
        self.client.login(email='test@test.ru', password='12345')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Сохранить')

    def test_profile_page_used_right_template(self):
        self.client.login(email='test@test.ru', password='12345')
        response = self.client.get(reverse('profile'))
        self.assertTemplateUsed(response, 'app_users/profile.html')

    def test_profile_page_access_without_login(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 403)


class MyLoginViewTest(TestCase):

    def test_login_page_exist_at_desired_location(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Войти')

    def test_login_page_used_right_template(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'app_users/login.html')


class ModalLoginViewTest(TestCase):

    def test_login_page_exist_at_desired_location(self):
        response = self.client.get(reverse('login_modal'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Войти')

    def test_login_page_used_right_template(self):
        response = self.client.get(reverse('login_modal'))
        self.assertTemplateUsed(response, 'app_users/login_modal.html')


class ValidateEmailTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(email='test@test.ru', phoneNumber='1234567890')
        user.set_password('12345')
        user.save()

    def test_validate_email_exist_at_desired_location(self):
        response = self.client.get(reverse('validate_email'))
        self.assertEqual(response.status_code, 200)

    def test_validate_email_page_take_only_get(self):
        response = self.client.post(reverse('validate_email'))
        self.assertEqual(response.status_code, 405)

    def test_get_order_status_response(self):
        response = self.client.get(reverse('validate_email'), {'email': 'test@test.ru'})
        self.assertEqual({'is_taken': True}, response.json())

class ValidatePhoneTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(email='test@test.ru', phoneNumber='1234567890')
        user.set_password('12345')
        user.save()

    def test_validate_email_exist_at_desired_location(self):
        response = self.client.get(reverse('validate_phone'))
        self.assertEqual(response.status_code, 200)

    def test_validate_email_page_take_only_get(self):
        response = self.client.post(reverse('validate_phone'))
        self.assertEqual(response.status_code, 405)

    def test_get_order_status_response(self):
        response = self.client.get(reverse('validate_phone'), {'phoneNumber': '1234567890'})
        self.assertEqual({'is_taken': True}, response.json())