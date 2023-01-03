import tempfile
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from app_shop.models import Category, Product, PropertyName, PropertyValue, Property
from app_review.models import Review
from app_users.models import User
from app_settings.models import SiteSettings
from app_orders.models import Order, OrderItem




class CategoryTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='test_category')
        category.save()
        product = Product.objects.create(name='test_product', id=1, category=category, price=10, stock=1,
                                         manufacturer='test_manufacturer')
        product.save()
        product2 = Product.objects.create(name='test_product2', id=2, category=category, price=100, stock=1,
                                          manufacturer='test_manufacturer')
        product2.save()

    def test_name_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Название')

    def test_slug_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'Псевдоним для url')

    def test_icon_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('icon').verbose_name
        self.assertEquals(field_label, 'Иконка')

    def test_parent_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('parent').verbose_name
        self.assertEquals(field_label, 'Родительская категория')

    def test_image_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('image').verbose_name
        self.assertEquals(field_label, 'Изображение')

    def test_name_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)

    def test_slug_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('slug').max_length
        self.assertEquals(max_length, 200)

    def test_icon_validator_svg(self):
        image = SimpleUploadedFile(tempfile.NamedTemporaryFile(suffix=".jpg").name, b"file_content",
                                   content_type="image/jpeg")
        category = Category.objects.create(name='test_category2', icon=image)
        with self.assertRaises(ValidationError, msg='Файл не svg'):
            category.full_clean()

    def test_get_min(self):
        category = Category.objects.get(id=1)
        self.assertEquals(category.get_min(), 10)


class ProductTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(email='test@test.ru')
        user.set_password('12345')
        user.save()
        category = Category.objects.create(name='test_category')
        category.save()
        settings = SiteSettings.objects.create(cost_express=500, edge_for_free_delivery=2000,
                                               cost_usual_delivery=200,
                                               root_category=category)
        settings.save()
        product = Product.objects.create(name='test_product', id=1, category=category, price=10, stock=1,
                                         manufacturer='test_manufacturer')
        product.save()
        review = Review.objects.create(user=user, product=product, text='test_review')
        review.save()
        order = Order.objects.create(user=user, address='test_address', city='test_city', card_number=888888888)
        order.save()
        order_item = OrderItem.objects.create(order=order, product=product, price=10, quantity=10)
        order_item.save()

    def test_category_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('category').verbose_name
        self.assertEquals(field_label, 'Категория')

    def test_name_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Название')

    def test_slug_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'Псевдоним для url')

    def test_description_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'Описание')

    def test_price_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('price').verbose_name
        self.assertEquals(field_label, 'Цена')

    def test_stock_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('stock').verbose_name
        self.assertEquals(field_label, 'Остаток')

    def test_available_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('available').verbose_name
        self.assertEquals(field_label, 'Активен')

    def test_created_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('created').verbose_name
        self.assertEquals(field_label, 'Создан')

    def test_updated_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('updated').verbose_name
        self.assertEquals(field_label, 'Обновлен')

    def test_manufacturer_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('manufacturer').verbose_name
        self.assertEquals(field_label, 'Производитель')

    def test_limited_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('limited').verbose_name
        self.assertEquals(field_label, 'Ограниченная серия')

    def test_name_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)

    def test_slug_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('slug').max_length
        self.assertEquals(max_length, 200)

    def test_price_max_digits(self):
        product = Product.objects.get(id=1)
        max_digits = product._meta.get_field('price').max_digits
        self.assertEquals(max_digits, 10)

    def test_price_decimal_places(self):
        product = Product.objects.get(id=1)
        decimal_places = product._meta.get_field('price').decimal_places
        self.assertEqual(decimal_places, 2)

    def test_manufacturer_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('manufacturer').max_length
        self.assertEquals(max_length, 50)

    def test_in_stock(self):
        product = Product.objects.get(id=1)
        self.assertTrue(product.in_stock)

    def test_total_review(self):
        product = Product.objects.get(id=1)
        self.assertEqual(1, product.total_review)

    def test_free_delivery(self):
        product = Product.objects.get(id=1)
        self.assertFalse(product.free_delivery)

    def test_total_sale(self):
        product = Product.objects.get(id=1)
        self.assertEqual(10, product.total_sale)

    def test_str(self):
        product = Product.objects.get(id=1)
        self.assertEqual(str(product), product.name)


class PropertyNameTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='test_category')
        category.save()
        product = Product.objects.create(name='test_product', id=1, category=category, price=10, stock=1,
                                         manufacturer='test_manufacturer')
        product.save()
        property = PropertyName.objects.create(name='test_property')
        property.save()

    def test_name_label(self):
        property = PropertyName.objects.get(id=1)
        field_label = property._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'характеристика')

    def test_name_max_length(self):
        property = PropertyName.objects.get(id=1)
        max_length = property._meta.get_field('name').max_length
        self.assertEquals(max_length, 255)


class PropertyValueTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='test_category')
        category.save()
        product = Product.objects.create(name='test_product', id=1, category=category, price=10, stock=1,
                                         manufacturer='test_manufacturer')
        product.save()
        value = PropertyValue.objects.create(value='test_value')
        value.save()

    def test_value_label(self):
        value = PropertyValue.objects.get(id=1)
        field_label = value._meta.get_field('value').verbose_name
        self.assertEquals(field_label, 'значение')

    def test_value_max_length(self):
        value = PropertyValue.objects.get(id=1)
        max_length = value._meta.get_field('value').max_length
        self.assertEquals(max_length, 255)


class PropertyTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='test_category')
        category.save()
        product = Product.objects.create(name='test_product', id=1, category=category, price=10, stock=1,
                                         manufacturer='test_manufacturer')
        product.save()
        value = PropertyValue.objects.create(value='test_value')
        value.save()
        property_name = PropertyName.objects.create(name='test_property')
        property_name.save()
        property = Property.objects.create(property=property_name, product=product, value=value)
        property.save()

    def test_property_label(self):
        property = Property.objects.get(id=1)
        field_label = property._meta.get_field('property').verbose_name
        self.assertEquals(field_label, 'название')

    def test_product_label(self):
        property = Property.objects.get(id=1)
        field_label = property._meta.get_field('product').verbose_name
        self.assertEquals(field_label, 'товар')

    def test_value_label(self):
        property = Property.objects.get(id=1)
        field_label = property._meta.get_field('value').verbose_name
        self.assertEquals(field_label, 'значение')

    def test_str(self):
        property = Property.objects.get(id=1)
        self.assertEqual(str(property), f'{property.property.name}: {property.value.value}')