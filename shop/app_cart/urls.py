from django.urls import path
from . import views
from .views import get_cart_data

urlpatterns = [path('cart_detail/', views.cart_detail.as_view(), name='cart_detail'),
               path('add/<int:pk>/', views.cart_add, name='cart_add'),
               path('remove/<int:pk>/', views.cart_remove, name='cart_remove'),
               path('get_cart_data/', get_cart_data, name='get_cart_data'),
               ]