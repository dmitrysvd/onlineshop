from django.urls import path

from . import views

app_name = 'onlinestore'

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.categories, name='categories'),
    path('products/<slug:category_slug>',
         views.product_list,
         name='product_list'),
    path('product/<slug:product_slug>',
         views.product_detail, name='product_detail'),
    path('shopcart/', views.shopcart, name='shopcart'),
]
