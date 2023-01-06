from django.contrib import admin

from .models import Cart_db


# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'quantity', 'price']


admin.site.register(Cart_db, CartAdmin)