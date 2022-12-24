from django.urls import path

from .views import payment

urlpatterns = [path('new/', payment, name='pay_new')
               ]