from django.contrib.auth import get_user, get_user_model
from django.db import models

from app_shop.models import Product

# Create your models here.
User = get_user_model()


class Cart_db(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='cart')
    good = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', related_name='cart')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return f'Корзина {self.user}'

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
