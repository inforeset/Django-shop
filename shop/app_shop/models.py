from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Min
from django.urls import reverse
from django.utils.text import slugify
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from .validators import is_svg
from app_settings.models import SiteSettings


def validate_svg(file):
    if not is_svg(file):
        raise ValidationError("File not svg")


class Category(MPTTModel):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    icon = models.FileField(upload_to='category/', blank=True, validators=[validate_svg])
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children',
                            db_index=True, verbose_name='Родительская категория')
    image = models.ImageField(blank=True, upload_to='category/')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = [['parent', 'slug']]
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product-by-category', args=[str(self.slug)])

    def get_min(self):
        sub_categories = self.get_descendants(include_self=True)
        price = Product.objects.values('price').filter(category__in=sub_categories).filter(available=True).aggregate(
            Min('price'))['price__min']
        return price

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name='category', verbose_name='Категория')
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, db_index=True, verbose_name='Слаг поле')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    stock = models.PositiveIntegerField(verbose_name='Остаток')
    available = models.BooleanField(default=True, verbose_name='Активен')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    manufacturer = models.CharField(max_length=50, db_index=True, verbose_name='Производитель')
    limited = models.BooleanField(default=False, verbose_name='Ограниченная серия')
    option = models.ManyToManyField('PropertyName', through="Property")

    @property
    def in_stock(self):
        return self.stock != 0

    @property
    def total_sale(self):
        return sum(item.quantity for item in self.order_items.all())

    @property
    def total_review(self):
        return len(self.review.all())

    @property
    def free_delivery(self):
        settings = SiteSettings.load()
        return self.price > settings.edge_for_free_delivery

    class Meta:
        ordering = ('price',)
        index_together = (('id', 'slug'),)
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.pk, self.slug])

    def __str__(self):
        return self.name


class PropertyName(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name='характеристика')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Имя характеристики"
        verbose_name_plural = "Имена характеристик"


class Property(models.Model):
    property = models.ForeignKey(PropertyName, on_delete=models.CASCADE, related_name='property',
                                 verbose_name='значение')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='товар', related_name='property')
    value = models.ForeignKey('PropertyValue', on_delete=models.CASCADE, verbose_name='значение',
                              related_name='property')

    def __str__(self):
        return f'{self.property.name}: {self.value.value}'

    class Meta:
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"


class PropertyValue(models.Model):
    value = models.CharField(max_length=255, verbose_name='значение')

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = "Значение характеристики"
        verbose_name_plural = "Значение характеристик"


class Gallery(models.Model):
    image = models.ImageField(upload_to='products/%Y/%m/%d')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='image', verbose_name='изображение')

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"
