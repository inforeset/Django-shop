from django.urls import path
from . import views

urlpatterns = [path('create/', views.OrderView.as_view(), name='create_order'),
               path('history/', views.HistoryOrders.as_view(), name='history'),
               path('<int:pk>/', views.OrderDetail.as_view(), name='order_detail'),
               path('order/status/', views.get_order_status, name='order_status'),
               path('pay/<int:pk>/', views.OrderPayment.as_view(), name='pay'),
               ]
