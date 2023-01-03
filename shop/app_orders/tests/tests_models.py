from django.test import TestCase
from app_shop.models import Category, Product
from app_users.models import User
from app_orders.models import OrderItem, Order


class OrderTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(email='test@test.ru')
        user.set_password('12345')
        user.save()
        order = Order.objects.create(user=user, address='test_address', city='test_city', card_number=888888888)
        order.save()
        category = Category.objects.create(name='test_category')
        category.save()
        product = Product.objects.create(name='test_product', id=1, category=category, price=10, stock=1,
                                         manufacturer='test_manufacturer')
        product.save()
        order_item = OrderItem.objects.create(order=order, product=product, price=10, quantity=10)
        order_item.save()

    def test_user_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'Пользователь')

    def test_address_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field('address').verbose_name
        self.assertEquals(field_label, 'Адрес')

    def test_address_max_length(self):
        order = Order.objects.get(id=1)
        max_length = order._meta.get_field('address').max_length
        self.assertEquals(max_length, 250)

    def test_city_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field('city').verbose_name
        self.assertEquals(field_label, 'Город')

    def test_city_max_length(self):
        order = Order.objects.get(id=1)
        max_length = order._meta.get_field('city').max_length
        self.assertEquals(max_length, 100)

    def test_delivery_type_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field('delivery_type').verbose_name
        self.assertEquals(field_label, 'Тип доставки')

    def test_delivery_type_max_length(self):
        order = Order.objects.get(id=1)
        max_length = order._meta.get_field('delivery_type').max_length
        self.assertEquals(max_length, 30)

    def test_delivery_price_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field('delivery_price').verbose_name
        self.assertEquals(field_label, 'Цена доставки')

    def test_delivery_price_max_digits(self):
        order = Order.objects.get(id=1)
        max_digits = order._meta.get_field('delivery_price').max_digits
        self.assertEquals(max_digits, 10)

    def test_delivery_price_decimal_places(self):
        order = Order.objects.get(id=1)
        decimal_places = order._meta.get_field('delivery_price').decimal_places
        self.assertEquals(decimal_places, 2)

    def test_payment_type_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field('payment_type').verbose_name
        self.assertEquals(field_label, 'Тип оплаты')

    def test_payment_type_max_length(self):
        order = Order.objects.get(id=1)
        max_length = order._meta.get_field('payment_type').max_length
        self.assertEquals(max_length, 30)

    def test_created_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field('created').verbose_name
        self.assertEquals(field_label, 'создан')

    def test_updated_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field('updated').verbose_name
        self.assertEquals(field_label, 'изменен')

    def test_paid_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field('paid').verbose_name
        self.assertEquals(field_label, 'оплачен')

    def test_card_number_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field('card_number').verbose_name
        self.assertEquals(field_label, 'Номер карты')

    def test_status_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field('status').verbose_name
        self.assertEquals(field_label, 'статус платежа')

    def test_status_max_length(self):
        order = Order.objects.get(id=1)
        max_length = order._meta.get_field('status').max_length
        self.assertEquals(max_length, 150)

    def test_payment_code_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field('payment_code').verbose_name
        self.assertEquals(field_label, 'Код оплаты')

    def test_get_total_cost(self):
        order = Order.objects.get(id=1)
        self.assertEquals(order.get_total_cost(), 100)

    def test_object_name(self):
        order = Order.objects.get(id=1)
        self.assertEquals(f'Заказ {order.id}', str(order))


class OrderItemTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(email='test@test.ru')
        user.set_password('12345')
        user.save()
        order = Order.objects.create(user=user, address='test_address', city='test_city', card_number=888888888)
        order.save()
        category = Category.objects.create(name='test_category')
        category.save()
        product = Product.objects.create(name='test_product', id=1, category=category, price=10, stock=1,
                                         manufacturer='test_manufacturer')
        product.save()
        order_item = OrderItem.objects.create(order=order, product=product, price=10, quantity=1)
        order_item.save()

    def test_order_label(self):
        order_item = OrderItem.objects.get(id=1)
        field_label = order_item._meta.get_field('order').verbose_name
        self.assertEquals(field_label, 'заказ')

    def test_product_label(self):
        order = OrderItem.objects.get(id=1)
        field_label = order._meta.get_field('product').verbose_name
        self.assertEquals(field_label, 'товар')

    def test_price_label(self):
        order_item = OrderItem.objects.get(id=1)
        field_label = order_item._meta.get_field('price').verbose_name
        self.assertEquals(field_label, 'цена')

    def test_price_max_digits(self):
        order_item = OrderItem.objects.get(id=1)
        max_digits = order_item._meta.get_field('price').max_digits
        self.assertEquals(max_digits, 10)

    def test_price_decimal_places(self):
        order_item = OrderItem.objects.get(id=1)
        decimal_places = order_item._meta.get_field('price').decimal_places
        self.assertEquals(decimal_places, 2)

    def test_quantity_label(self):
        order_item = OrderItem.objects.get(id=1)
        field_label = order_item._meta.get_field('quantity').verbose_name
        self.assertEquals(field_label, 'Количество')

    def test_get_cost(self):
        order_item = OrderItem.objects.get(id=1)
        self.assertEquals(order_item.get_cost(), 10)

    def test_object_name(self):
        order_item = OrderItem.objects.get(id=1)
        self.assertEquals(str(order_item.id), str(order_item))
