from django.db import OperationalError
from django.db.models import Min, Max, QuerySet
from .models import Product, Category

from app_settings.models import SiteSettings


def get_data_min(root_category: Category, queryset: QuerySet = None) -> int:
    min_price = 0
    if queryset:
        min_price = queryset.values('price').aggregate(Min('price'))['price__min']
    else:
        try:
            sub_categories = root_category.get_descendants(include_self=True)
            min_price = \
                Product.objects.values('price').filter(category__in=sub_categories).filter(available=True).aggregate(
                    Min('price'))['price__min']
        except (AttributeError, OperationalError) as exc:
            pass
    return int(min_price)


def get_data_max(root_category, queryset: QuerySet = None) -> int:
    max_price = 0
    if queryset:
        max_price = queryset.values('price').aggregate(Max('price'))['price__max']
    else:
        try:
            sub_categories = root_category.get_descendants(include_self=True)
            max_price = \
                Product.objects.values('price').filter(category__in=sub_categories).filter(available=True).aggregate(
                    Max('price'))['price__max']
        except (AttributeError, OperationalError) as exc:
            pass
    return max_price
