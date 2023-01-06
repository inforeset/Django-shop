from django.test import TestCase
from app_shop.models import Category, Product
from app_users.models import User
from app_review.models import Review


class ReviewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(email='test@test.ru')
        user.set_password('12345')
        user.save()
        category = Category.objects.create(name='test_category')
        category.save()
        product = Product.objects.create(name='test_product', id=1, category=category, price=10, stock=1,
                                         manufacturer='test_manufacturer')
        product.save()
        review = Review.objects.create(user=user, product=product, text='test_review')
        review.save()

    def test_user_label(self):
        order = Review.objects.get(id=1)
        field_label = order._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'Пользователь')

    def test_product_label(self):
        order = Review.objects.get(id=1)
        field_label = order._meta.get_field('product').verbose_name
        self.assertEquals(field_label, 'товар')

    def test_text_label(self):
        order = Review.objects.get(id=1)
        field_label = order._meta.get_field('text').verbose_name
        self.assertEquals(field_label, 'отзыв')

    def test_text_max_length(self):
        order = Review.objects.get(id=1)
        max_length = order._meta.get_field('text').max_length
        self.assertEquals(max_length, 300)

    def test_object_name(self):
        order = Review.objects.get(id=1)
        self.assertEquals(f'Отзывы к {order.product.name}', str(order))