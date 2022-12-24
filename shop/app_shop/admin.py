from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import Category, Product, Gallery, PropertyValue, Property, PropertyName


class PropertyValueInline(admin.TabularInline):
    model = Property


class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery


class CategoryAdmin(DjangoMpttAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created',
                    'updated']
    list_filter = ['category', 'available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [GalleryInline, PropertyValueInline]


admin.site.register(Product, ProductAdmin)

admin.site.register(Property)
admin.site.register(PropertyName)
admin.site.register(PropertyValue)