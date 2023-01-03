from django.test import TestCase
from app_shop.models import Category
from app_settings.models import SiteSettings


class SiteSettingsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='test_category')
        category.save()
        settings = SiteSettings.objects.create(cost_express=500, edge_for_free_delivery=2000,
                                               cost_usual_delivery=200,
                                               root_category=category)
        settings.save()

    def test_cost_express_label(self):
        settings = SiteSettings.objects.get(id=1)
        field_label = settings._meta.get_field('cost_express').verbose_name
        self.assertEquals(field_label, 'Цена экспресс доставки')

    def test_edge_for_free_delivery_label(self):
        settings = SiteSettings.objects.get(id=1)
        field_label = settings._meta.get_field('edge_for_free_delivery').verbose_name
        self.assertEquals(field_label, 'Порог бесплатной доставки')

    def test_cost_usual_delivery_label(self):
        settings = SiteSettings.objects.get(id=1)
        field_label = settings._meta.get_field('cost_usual_delivery').verbose_name
        self.assertEquals(field_label, 'Цена обычной доставки')

    def test_root_category_label(self):
        settings = SiteSettings.objects.get(id=1)
        field_label = settings._meta.get_field('root_category').verbose_name
        self.assertEquals(field_label, 'Корневая категория каталога')

    def test_category_main_page_label(self):
        settings = SiteSettings.objects.get(id=1)
        field_label = settings._meta.get_field('category_main_page').verbose_name
        self.assertEquals(field_label, 'Категории для показа на главной странице (не больше 3)')

    def test_quantity_popular_label(self):
        settings = SiteSettings.objects.get(id=1)
        field_label = settings._meta.get_field('quantity_popular').verbose_name
        self.assertEquals(field_label, 'Количество популярных товаров на главной странице')

    def test_time_cache_product_label(self):
        settings = SiteSettings.objects.get(id=1)
        field_label = settings._meta.get_field('time_cache_product').verbose_name
        self.assertEquals(field_label, 'Через какое кол-во дней кэшировать данные о продукте')

    def test_cost_express_max_digits(self):
        settings = SiteSettings.objects.get(id=1)
        max_length = settings._meta.get_field('cost_express').max_digits
        self.assertEquals(max_length, 10)

    def test_cost_express_decimal_places(self):
        settings = SiteSettings.objects.get(id=1)
        max_length = settings._meta.get_field('cost_express').decimal_places
        self.assertEquals(max_length, 2)

    def test_edge_for_free_delivery_max_digits(self):
        settings = SiteSettings.objects.get(id=1)
        max_length = settings._meta.get_field('edge_for_free_delivery').max_digits
        self.assertEquals(max_length, 10)

    def test_edge_for_free_delivery_decimal_places(self):
        settings = SiteSettings.objects.get(id=1)
        max_length = settings._meta.get_field('edge_for_free_delivery').decimal_places
        self.assertEquals(max_length, 2)

    def test_cost_usual_delivery_max_digits(self):
        settings = SiteSettings.objects.get(id=1)
        max_length = settings._meta.get_field('cost_usual_delivery').max_digits
        self.assertEquals(max_length, 10)

    def test_cost_usual_delivery_decimal_places(self):
        settings = SiteSettings.objects.get(id=1)
        max_length = settings._meta.get_field('cost_usual_delivery').decimal_places
        self.assertEquals(max_length, 2)

    def model_is_singleton(self):
        category = Category.objects.create(name='test_category2')
        category.save()
        settings = SiteSettings.objects.create(cost_express=100, edge_for_free_delivery=100,
                                               cost_usual_delivery=100,
                                               root_category=category)
        settings.save()
        self.assertEqual(settings.id, 1)
