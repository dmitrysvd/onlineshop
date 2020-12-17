from django.contrib import admin
from .models import Category, Product, Brand


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'sale', 'discount_price',
                    'available', 'created', 'updated')
    list_editable = ('price', 'discount_price', 'sale', 'available')
    list_filter = ('category', 'available', 'sale')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('price', 'discount_price', 'created', 'updated')


admin.site.register(Brand)
