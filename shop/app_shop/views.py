from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.http import urlencode
from django.core.cache import cache

# Create your views here.
from django.views import generic
from django.views.generic import DetailView, TemplateView
from django_filters.views import FilterView

from .filters import ProductFilter
from .models import Product, Category
from app_cart.forms import CartAddProductForm

from app_review.forms import ReviewForm

from .utils_shop import get_data_min, get_data_max
from app_settings.models import SiteSettings

from app_review.models import Review


class ShopView(TemplateView):
    template_name = 'app_shop/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Product.objects.select_related('category').filter(available=True). \
            only('category', 'name', 'price')
        list_product = [(item, item.total_sale) for item in queryset]
        quantity = SiteSettings.load()
        context['products'] = sorted(list_product, key=lambda product: product[1], reverse=True)[
                              :quantity.quantity_popular]
        context['limited'] = queryset.filter(limited=True)
        return context


class AccountView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'app_shop/account.html'
    raise_exception = True


class CatalogView(generic.ListView):
    paginate_by = 8
    model = Product
    template_name = 'app_shop/catalog.html'


class ProductByCategoryView(FilterView):
    paginate_by = 8
    model = Product
    context_object_name = 'products'
    template_name = 'app_shop/catalog.html'
    filterset_class = ProductFilter

    def get_queryset(self):
        settings = SiteSettings.load()
        self.category = settings.root_category
        sub_categories = self.category.get_descendants(include_self=True)
        queryset = Product.objects.filter(category__in=sub_categories).filter(available=True)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.category
        qs = self.get_queryset()
        min_price = get_data_min(qs)
        max_price = get_data_max(qs)
        context['filter'].form.fields['price'].widget.attrs = {'class': 'range-line',
                                                               'data-type': 'double',
                                                               'data-min': min_price,
                                                               'data-max': max_price}
        return context


class ProductView(DetailView):
    model = Product
    template_name = 'app_shop/product.html'

    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        context['form'] = CartAddProductForm(initial={'quantity': 1})
        context['reviews'] = Review.objects.filter(product=self.get_object()).order_by('-created')
        return context

    def get_object(self, queryset=None):
        time_cache = SiteSettings.load().time_cache_product
        if not time_cache:
            time_cache = 1
        return cache.get_or_set(f'product:{self.kwargs.get("pk")}',
                                Product.objects.get(id=self.kwargs.get("pk")), 60 * 60 * time_cache)

    def post(self, request, pk, slug):
        form = ReviewForm(request.POST)
        if not request.user.is_authenticated:
            raise PermissionDenied()
        if form.is_valid:
            review = form.save(commit=False)
            review.user = request.user
            review.product = self.get_object()
            review.save()
            messages.success(request, 'Отзыв добавлен')
        return HttpResponseRedirect(reverse('product_detail', kwargs={"pk": pk, "slug": slug}))
