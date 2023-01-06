from contextlib import suppress

import django_filters
from django import forms
from django.db import OperationalError
from django_property_filter import PropertyBooleanFilter, PropertyFilterSet, PropertyOrderingFilter

from .models import Product
from .shop_widgets import ShopLinkWidget, ShopCheckboxInput
from .utils_shop import get_data_min, get_data_max
from app_settings.models import SiteSettings


class ProductFilter(PropertyFilterSet):
    root_category = 1
    with suppress(OperationalError):
        settings = SiteSettings.load()
        root_category = settings.root_category
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', widget=forms.TextInput(
        attrs={'class': 'form-input form-input_full',
               'placeholder': 'Название'}))
    manufacturer = django_filters.CharFilter(
        field_name='manufacturer', lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-input form-input_full', 'placeholder': 'Производитель'}))
    in_stock = PropertyBooleanFilter(field_name='in_stock', widget=ShopCheckboxInput)
    delivery = PropertyBooleanFilter(field_name='free_delivery', widget=ShopCheckboxInput)
    limited = PropertyBooleanFilter(field_name='limited', widget=ShopCheckboxInput)
    price = django_filters.CharFilter(method='price_range', field_name='price', lookup_expr='range',
                                      widget=forms.TextInput(attrs={'class': 'range-line',
                                                                    'data-type': 'double',
                                                                    'data-min': get_data_min(
                                                                        root_category=root_category),
                                                                    'data-max': get_data_max(
                                                                        root_category=root_category)}))

    order_by_field = 'ordering'
    ordering = PropertyOrderingFilter(
        choices=(('price', 'Цене'), ('-price', 'Цене'), ('updated', 'Новизне'), ('-updated', 'Новизне'),
                 ('total_sale', 'Популярности'), ('-total_sale', 'Популярности'),
                 ('total_review', 'Отзывам'), ('-total_review', 'Отзывам')),
        fields=['price', 'updated', 'total_sale', 'total_review'],
        empty_label=None,
        widget=ShopLinkWidget)

    @staticmethod
    def price_range(queryset, _, value):
        return queryset.filter(price__range=value.split(';'))

    class Meta:
        model = Product
        order_by_field = 'price'
        fields = ('price', 'name', 'in_stock', 'delivery', 'manufacturer')
