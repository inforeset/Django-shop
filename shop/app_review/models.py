from django.contrib.auth import get_user_model
from django.db import models

from app_shop.models import Product

User = get_user_model()


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='review')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='товар', related_name='review')
    text = models.TextField(verbose_name='отзыв')
    created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')

    def __str__(self):
        return f'Отзывы к {self.product.name}'

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"