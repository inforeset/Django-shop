from django.contrib.messages import get_messages
from django.test import TestCase, RequestFactory
from django.urls import reverse
from app_shop.models import Category, Product
from app_users.models import User
from app_settings.models import SiteSettings
from app_cart.models import Cart_db
from app_users.forms import UserCreateForm
from app_orders.models import Order, OrderItem
from app_orders.views import HistoryOrders


class TestOrderView(TestCase):

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
        settings = SiteSettings.objects.create(cost_express=500, edge_for_free_delivery=2000, cost_usual_delivery=200,
                                               root_category=category)
        settings.save()
        cart = Cart_db.objects.create(user=user, good=product, quantity=1, price=10)
        cart.save()

    def test_order_page_exist_at_desired_location(self):
        self.client.login(email='test@test.ru', password='12345')
        response = self.client.get(reverse('create_order'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Шаг 1. Параметры пользователя')

    def test_order_page_used_right_template(self):
        self.client.login(email='test@test.ru', password='12345')
        response = self.client.get(reverse('create_order'))
        self.assertTemplateUsed(response, 'app_orders/order.html')

    def test_order_page_access(self):
        response = self.client.get(reverse('create_order'))
        self.assertEqual(response.status_code, 200)

    def test_order_page_contain_right_context(self):
        self.client.login(email='test@test.ru', password='12345')
        settings = SiteSettings.load()
        response = self.client.get(reverse('create_order'))
        price_usual = response.context.get('price_usual')
        self.assertEqual(settings.cost_usual_delivery, price_usual)
        form_reg = response.context.get('form_reg')
        self.assertTrue(form_reg.fields['email'].disabled)
        self.assertTrue(form_reg.fields['full_name'].disabled)
        self.assertTrue(form_reg.fields['phoneNumber'].disabled)
        self.assertEqual(form_reg.__class__.__name__, UserCreateForm().__class__.__name__)

    def test_order_page_post(self):
        self.client.login(email='test@test.ru', password='12345')
        response = self.client.post(reverse('create_order'), {'address': 'test_address', 'city': 'test_city',
                                                              'card_number': '88888888', 'delivery_type': '1',
                                                              'payment_type': '1'})
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(email='test@test.ru')
        self.assertFalse(Cart_db.objects.filter(user=user).exists())
        self.assertTrue(Order.objects.get(id=1))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[0]), 'Заказ успешно добавлен.')
        self.assertEqual(str(messages[1]), 'Ждём подтверждения оплаты от платёжной системы.')


class TestHistoryView(TestCase):

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
        settings = SiteSettings.objects.create(cost_express=500, edge_for_free_delivery=2000,
                                               cost_usual_delivery=200,
                                               root_category=category)
        settings.save()
        order = Order.objects.create(user=user, address='test_address', city='test_city', card_number=888888888)
        order.save()
        order_item = OrderItem.objects.create(order=order, product=product, price=10, quantity=10)
        order_item.save()

    def test_history_page_exist_at_desired_location(self):
        self.client.login(email='test@test.ru', password='12345')
        response = self.client.get(reverse('history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Общая стоимость:')

    def test_history_page_used_right_template(self):
        self.client.login(email='test@test.ru', password='12345')
        response = self.client.get(reverse('history'))
        self.assertTemplateUsed(response, 'app_orders/historyorder.html')

    def test_history_page_without_login(self):
        response = self.client.get(reverse('history'))
        self.assertEqual(response.status_code, 403)

    def test_history_page_get_queryset(self):
        self.client.login(email='test@test.ru', password='12345')
        user = User.objects.get(email='test@test.ru')
        request = RequestFactory().get(reverse('history'))
        request.user = user
        view = HistoryOrders()
        view.request = request
        qs = view.get_queryset()
        self.assertQuerysetEqual(qs, Order.objects.filter(user=user).all())


class TestOrderDetailView(TestCase):

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
        user2 = User.objects.create(email='test2@test.ru', phoneNumber=123)
        user2.set_password('123456')
        user2.save()
        settings = SiteSettings.objects.create(cost_express=500, edge_for_free_delivery=2000,
                                               cost_usual_delivery=200,
                                               root_category=category)
        settings.save()
        order = Order.objects.create(user=user, address='test_address', city='test_city', card_number=888888888)
        order.save()
        order_item = OrderItem.objects.create(order=order, product=product, price=10, quantity=10)
        order_item.save()

    def test_order_detail_page_exist_at_desired_location(self):
        self.client.login(email='test@test.ru', password='12345')
        response = self.client.get(reverse('order_detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Заказ №1')

    def test_order_detail_page_used_right_template(self):
        self.client.login(email='test@test.ru', password='12345')
        response = self.client.get(reverse('order_detail', args=[1]))
        self.assertTemplateUsed(response, 'app_orders/oneorder.html')

    def test_order_detail_page_without_login(self):
        response = self.client.get(reverse('order_detail', args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_order_detail_page_try_to_access_to_order_another_user(self):
        self.client.login(email='test2@test.ru', password='123456')
        response = self.client.get(reverse('order_detail', args=[1]))
        self.assertEqual(response.status_code, 403)


class OrderPaymentView(TestCase):

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
        user2 = User.objects.create(email='test2@test.ru', phoneNumber=123)
        user2.set_password('123456')
        user2.save()
        settings = SiteSettings.objects.create(cost_express=500, edge_for_free_delivery=2000,
                                               cost_usual_delivery=200,
                                               root_category=category)
        settings.save()
        order = Order.objects.create(user=user, address='test_address', city='test_city', card_number=888888888)
        order.save()
        order_item = OrderItem.objects.create(order=order, product=product, price=10, quantity=10)
        order_item.save()

    def test_pay_page_exist_at_desired_location(self):
        self.client.login(email='test@test.ru', password='12345')
        response = self.client.get(reverse('pay', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_pay_page_used_right_template(self):
        self.client.login(email='test@test.ru', password='12345')
        response = self.client.get(reverse('pay', args=[1]))
        self.assertTemplateUsed(response, 'app_orders/payment.html')

    def test_pay_page_without_login(self):
        response = self.client.get(reverse('pay', args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_pay_page_try_to_access_to_order_another_user(self):
        self.client.login(email='test2@test.ru', password='123456')
        response = self.client.get(reverse('pay', args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_pay_page_post(self):
        self.client.login(email='test@test.ru', password='12345')
        response = self.client.post(reverse('pay', args=[1]), {'card_number': '88888888', 'payment_type': '1'})
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Ждём подтверждения оплаты от платёжной системы.')


class GetOrderStatusView(TestCase):

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
        settings = SiteSettings.objects.create(cost_express=500, edge_for_free_delivery=2000,
                                               cost_usual_delivery=200,
                                               root_category=category)
        settings.save()
        order = Order.objects.create(user=user, address='test_address', city='test_city', card_number=888888888)
        order.save()
        order_item = OrderItem.objects.create(order=order, product=product, price=10, quantity=10)
        order_item.save()

    def test_get_order_status_exist_at_desired_location(self):
        self.client.login(email='test@test.ru', password='12345')
        response = self.client.get(reverse('order_status'))
        self.assertEqual(response.status_code, 200)

    def test_get_order_status_page_take_only_get(self):
        self.client.login(email='test@test.ru', password='12345')
        response = self.client.post(reverse('order_status'))
        self.assertEqual(response.status_code, 405)

    def test_get_order_status_page_without_user(self):
        response = self.client.get(reverse('order_status'), {'order_id': '1'})
        self.assertEqual(response.status_code, 302)

    def test_get_order_status_response(self):
        self.client.login(email='test@test.ru', password='12345')
        response = self.client.get(reverse('order_status'), {'order_id': '1'})
        self.assertEqual({'status': None, 'code': 0}, response.json())
