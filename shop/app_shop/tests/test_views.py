from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from app_settings.models import SiteSettings
from app_shop.models import Category, Product
from app_users.models import User
from app_cart.forms import CartAddProductForm
from app_review.forms import ReviewForm
from app_review.models import Review



class TestShopView(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='test_category')
        category.save()
        settings = SiteSettings.objects.create(cost_express=500, edge_for_free_delivery=2000, cost_usual_delivery=200,
                                               root_category=category)
        settings.save()
        product = Product.objects.create(name='test_product', id=1, category=category, price=10, stock=1,
                                         manufacturer='test_manufacturer', limited=True)
        product.save()

    def test_main_page_exist_at_desired_location(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Гарантированные платежи')

    def test_main_page_used_right_template(self):
        response = self.client.get(reverse('main'))
        self.assertTemplateUsed(response, 'app_shop/index.html')

    def test_main_page_contain_right_context(self):
        self.client.login(email='test@test.ru', password='12345')
        response = self.client.get(reverse('main'))
        products = response.context.get('products')
        limited = response.context.get('limited')
        self.assertEqual(1, len(products))
        self.assertEqual(1, len(limited))


class TestAccountView(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(email='test@test.ru')
        user.set_password('12345')
        user.save()

    def test_account_page_exist_at_desired_location(self):
        self.client.login(email='test@test.ru', password='12345')
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Редактировать профиль')

    def test_account_page_used_right_template(self):
        self.client.login(email='test@test.ru', password='12345')
        response = self.client.get(reverse('account'))
        self.assertTemplateUsed(response, 'app_shop/account.html')

    def test_account_page_access_without_login(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(403, response.status_code)


class TestProductByCategoryView(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='test_category')
        category.save()
        settings = SiteSettings.objects.create(cost_express=500, edge_for_free_delivery=2000, cost_usual_delivery=200,
                                               root_category=category)
        settings.save()
        product = Product.objects.create(name='test_product', id=1, category=category, price=10, stock=1,
                                         manufacturer='test_manufacturer', limited=True)
        product.save()

    def test_catalog_page_exist_at_desired_location(self):
        response = self.client.get(reverse('catalog'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Сортировать по:')

    def test_catalog_page_used_right_template(self):
        response = self.client.get(reverse('catalog'))
        self.assertTemplateUsed(response, 'app_shop/catalog.html')

    def test_catalog_page_context(self):
        response = self.client.get(reverse('catalog'))
        title = response.context.get('title')
        self.assertEqual('test_category', str(title))
        filter = response.context.get('filter')
        self.assertEqual(filter.form.fields['price'].widget.attrs['data-max'], 10)
        self.assertEqual(filter.form.fields['price'].widget.attrs['data-min'], 10)


class TestProductView(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(email='test@test.ru')
        user.set_password('12345')
        user.save()
        category = Category.objects.create(name='test_category')
        category.save()
        settings = SiteSettings.objects.create(cost_express=500, edge_for_free_delivery=2000, cost_usual_delivery=200,
                                               root_category=category)
        settings.save()
        product = Product.objects.create(name='test_product', id=1, category=category, price=10, stock=1,
                                         manufacturer='test_manufacturer', limited=True)
        product.save()
        review = Review.objects.create(user=user, product=product, text='test_review')
        review.save()

    def test_product_page_exist_at_desired_location(self):
        response = self.client.get(reverse('product_detail', args=[1, 'test_product']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test_manufacturer')

    def test_product_page_used_right_template(self):
        response = self.client.get(reverse('product_detail', args=[1, 'test_product']))
        self.assertTemplateUsed(response, 'app_shop/product.html')

    def test_product_page_context(self):
        response = self.client.get(reverse('product_detail', args=[1, 'test_product']))
        context = response.context
        self.assertEqual(context['review_form'].__class__.__name__, ReviewForm().__class__.__name__)
        self.assertEqual(context['form'].__class__.__name__, CartAddProductForm().__class__.__name__)
        self.assertEqual(context['reviews'].first().__class__.__name__, Review().__class__.__name__)

    def test_product_page_post(self):
        self.client.login(email='test@test.ru', password='12345')
        response = self.client.post(reverse('product_detail', args=[1, 'test_product']),
                                    {'text': 'test_review'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Review.objects.all()), 2)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Отзыв добавлен')
