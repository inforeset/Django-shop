from django.test import TestCase
from app_cart.models import Cart_db
from app_shop.models import Category, Product
from app_users.models import User


class CartDbTest(TestCase):

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
        cart = Cart_db.objects.create(user=user, good=product, quantity=1, price=10)
        cart.save()

    def test_user_label(self):
        record = Cart_db.objects.get(id=1)
        field_label = record._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'Пользователь')

    def test_good_label(self):
        record = Cart_db.objects.get(id=1)
        field_label = record._meta.get_field('good').verbose_name
        self.assertEquals(field_label, 'Товар')

    def test_quantity_label(self):
        record = Cart_db.objects.get(id=1)
        field_label = record._meta.get_field('quantity').verbose_name
        self.assertEquals(field_label, 'Количество')

    def test_price_label(self):
        record = Cart_db.objects.get(id=1)
        field_label = record._meta.get_field('price').verbose_name
        self.assertEquals(field_label, 'Цена')

    def test_object_name(self):
        user = User.objects.get(email='test@test.ru')
        record = Cart_db.objects.get(id=1)
        self.assertEquals(f'Корзина {user}', str(record))

    def test_price_max_digits(self):
        record = Cart_db.objects.get(id=1)
        max_digits = record._meta.get_field('price').max_digits
        self.assertEquals(max_digits, 10)

    def test_price_decimal_places(self):
        record = Cart_db.objects.get(id=1)
        decimal_places = record._meta.get_field('price').decimal_places
        self.assertEquals(decimal_places, 2)