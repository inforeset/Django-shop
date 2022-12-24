from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from app_shop.models import Product
from app_users.models import User


class Order(models.Model):
    DELIVERY_CHOICES = (
        ("1", "Обычная доставка"),
        ("2", "Экспресс доставка"),
    )

    PAYMENT_CHOICES = (
        ("1", "Онлайн картой"),
        ("2", "Онлайн со случайного чужого счета"),
    )

    user = models.ForeignKey(User, related_name='order', on_delete=models.CASCADE, verbose_name='Пользователь')
    address = models.CharField(max_length=250, verbose_name='Адрес')
    city = models.CharField(max_length=100, verbose_name='Город')
    delivery_type = models.CharField(max_length=30, choices=DELIVERY_CHOICES, verbose_name='Тип доставки',
                                     default="1")
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена доставки', default=0)
    payment_type = models.CharField(max_length=30, choices=PAYMENT_CHOICES, verbose_name='Тип оплаты',
                                    default="1")
    created = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='изменен')
    paid = models.BooleanField(default=False, verbose_name='оплачен')
    card_number = models.PositiveIntegerField(validators=[MinValueValidator(10000000), MaxValueValidator(99999999)],
                                              verbose_name='Номер карты')
    status = models.CharField(max_length=150, verbose_name='статус платежа', blank=True, null=True)
    payment_code = models.IntegerField(default=0, verbose_name='Код оплаты')

    class Meta:
        ordering = ('-created',)
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return 'Заказ {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all()) + self.delivery_price


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='заказ')
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name='товар')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = "Товары"
        verbose_name_plural = "Товары"
