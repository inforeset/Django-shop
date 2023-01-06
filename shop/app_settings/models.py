from django.db import models

from .singleton_model import SingletonModel


class SiteSettings(SingletonModel):
    cost_express = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена экспресс доставки')
    edge_for_free_delivery = models.DecimalField(max_digits=10, decimal_places=2,
                                                 verbose_name='Порог бесплатной доставки')
    cost_usual_delivery = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена обычной доставки')
    root_category = models.ForeignKey('app_shop.Category', on_delete=models.CASCADE,
                                      verbose_name='Корневая категория каталога', related_name='root_category',
                                      blank=True, null=True)
    category_main_page = models.ManyToManyField('app_shop.Category',
                                                verbose_name='Категории для показа на главной странице (не больше 3)')
    quantity_popular = models.PositiveIntegerField(verbose_name='Количество популярных товаров на главной странице',
                                                   default=8)
    time_cache_product = models.PositiveIntegerField(
        verbose_name='Через какое кол-во дней кэшировать данные о продукте', default=1)

    def __str__(self):
        return 'Конфигурация'

    class Meta:
        verbose_name = "Конфигурация"
        verbose_name_plural = "Конфигурация"
