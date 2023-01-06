from django.test import TestCase
from app_shop.models import Product, Category
from django.urls import reverse
from shop import settings
from app_cart.models import Cart_db
from app_users.models import User


class CartAddTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='test_category')
        category.save()
        product = Product.objects.create(name='test_product', id=1, category=category, price=10, stock=1,
                                         manufacturer='test_manufacturer')
        product.save()
        user = User.objects.create(email='test@test.ru')
        user.set_password('12345')
        user.save()

    def test_cart_add_page_exist_at_desired_location(self):
        response = self.client.post(reverse('cart_add', args=[1]), {'quantity': 1, 'update_quantity=': False})
        self.assertEqual(response.status_code, 302)

    def test_cart_add_page_take_only_post(self):
        response = self.client.get(reverse('cart_add', args=[1]), {'quantity': 1, 'update_quantity=': False})
        self.assertEqual(response.status_code, 405)

    def test_cart_add_view_without_user(self):
        self.client.post(reverse('cart_add', args=[1]), {'quantity': 1, 'update_quantity=': False})
        session = self.client.session
        self.assertIsNotNone(session.get(settings.CART_SESSION_ID))
        self.assertEqual(1, len(session[settings.CART_SESSION_ID]))
        self.assertIsNotNone(session.get(settings.CART_SESSION_ID, {}).get('1'))

    def test_cart_add_view_with_user(self):
        self.client.post(reverse('cart_add', args=[1]), {'quantity': 1, 'update_quantity=': False})
        self.client.login(email='test@test.ru', password='12345')
        self.client.post(reverse('cart_add', args=[1]), {'quantity': 1, 'update_quantity=': False})
        session = self.client.session
        product = Product.objects.get(pk=1)
        cart = Cart_db.objects.get(good=product)
        self.assertIsNone(session.get(settings.CART_SESSION_ID))
        self.assertEqual(cart.quantity, 2)


class CartRemoveTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='test_category')
        category.save()
        product = Product.objects.create(name='test_product', id=1, category=category, price=10, stock=1,
                                         manufacturer='test_manufacturer')
        product.save()
        user = User.objects.create(email='test@test.ru')
        user.set_password('12345')
        user.save()

    def test_cart_remove_page_exist_at_desired_location(self):
        response = self.client.get(reverse('cart_remove', args=[1]))
        self.assertEqual(response.status_code, 302)

    def test_cart_remove_page_take_only_get(self):
        self.client.login(email='test@test.ru', password='12345')
        response = self.client.post(reverse('cart_remove', args=[1]))
        self.assertEqual(response.status_code, 405)

    def test_cart_remove_view_without_user(self):
        self.client.post(reverse('cart_add', args=[1]), {'quantity': 1, 'update_quantity=': False})
        session = self.client.session
        self.assertIsNotNone(session.get(settings.CART_SESSION_ID))
        self.client.get(reverse('cart_remove', args=[1]))
        session = self.client.session
        self.assertFalse(session.get(settings.CART_SESSION_ID))

    def test_cart_remove_view_with_user(self):
        self.client.login(email='test@test.ru', password='12345')
        self.client.post(reverse('cart_add', args=[1]), {'quantity': 1, 'update_quantity=': False})
        session = self.client.session
        self.assertIsNone(session.get(settings.CART_SESSION_ID))
        product = Product.objects.get(pk=1)
        item_cart = Cart_db.objects.get(good=product)
        self.assertIsNotNone(item_cart)
        self.client.get(reverse('cart_remove', args=[1]))
        item_cart = Cart_db.objects.filter(good=product)
        self.assertFalse(item_cart)


class GetCartDataTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='test_category')
        category.save()
        product = Product.objects.create(name='test_product', id=1, category=category, price=10, stock=1,
                                         manufacturer='test_manufacturer')
        product.save()

    def test_cart_data_page_exist_at_desired_location(self):
        self.client.post(reverse('cart_add', args=[1]), {'quantity': 1, 'update_quantity=': False})
        response = self.client.get(reverse('get_cart_data'), {'product': 1})
        self.assertEqual(response.status_code, 200)

    def test_cart_data_page_take_only_get(self):
        self.client.post(reverse('cart_add', args=[1]), {'quantity': 1, 'update_quantity=': False})
        response = self.client.post(reverse('get_cart_data'), {'product': 1})
        self.assertEqual(response.status_code, 405)

    def test_get_cart_data_view(self):
        self.client.post(reverse('cart_add', args=[1]), {'quantity': 1, 'update_quantity=': False})
        response = self.client.get(reverse('get_cart_data'), {'product': 1})
        self.assertEqual({'total_len': 1, 'total': '10.00', 'total_item': '10.00'}, response.json())


class CartDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='test_category')
        category.save()
        product = Product.objects.create(name='test_product', id=1, category=category, price=10, stock=1,
                                         manufacturer='test_manufacturer')
        product.save()

    def test_cart_detail_page_exist_at_desired_location(self):
        response = self.client.get(reverse('cart_detail'))
        self.assertEqual(response.status_code, 200)

    def test_cart_detail_page_used_right_template(self):
        response = self.client.get(reverse('cart_detail'))
        self.assertTemplateUsed(response, 'app_cart/cart.html')

    def test_cart_detail_page_contain_right_context(self):
        self.client.post(reverse('cart_add', args=[1]), {'quantity': 1, 'update_quantity=': False})
        response = self.client.get(reverse('cart_detail'))
        cart = response.context.get('cart')
        self.assertIsNotNone(cart)
        for item in cart:
            self.assertIsNotNone(item.get('update_quantity_form'))