from django.urls import path

from .views import ShopView, AccountView, ProductByCategoryView, ProductView

urlpatterns = [path('', ShopView.as_view(), name='main'),
               path('account/', AccountView.as_view(), name='account'),
               path('catalog/', ProductByCategoryView.as_view(), name='catalog'),
               path('catalog/<str:slug>/', ProductByCategoryView.as_view(), name='product-by-category'),
               path('good/<int:pk>/<str:slug>/', ProductView.as_view(), name='product_detail')
               ]
