from contextlib import suppress

from django.db.models import Min, Max, QuerySet
from .models import Product, Category


def get_data_min(root_category: Category, queryset: QuerySet = None) -> int:
    if queryset:
        min_price = queryset.values('price').aggregate(Min('price'))['price__min']
    else:
        with suppress(AttributeError):
            sub_categories = root_category.get_descendants(include_self=True)
            min_price = \
                Product.objects.values('price').filter(category__in=sub_categories).filter(available=True).aggregate(
                    Min('price'))['price__min']
        if not min_price:
            return 0
    return int(min_price)


def get_data_max(root_category, queryset: QuerySet = None) -> int:
    if queryset:
        max_price = queryset.values('price').aggregate(Max('price'))['price__max']
    else:
        with suppress(AttributeError):
            sub_categories = root_category.get_descendants(include_self=True)
            max_price = \
                Product.objects.values('price').filter(category__in=sub_categories).filter(available=True).aggregate(
                    Max('price'))['price__max']
        if not max_price:
            return 0
    return max_price
