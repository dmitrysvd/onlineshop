from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('categories/', views.categories, name='categories'),
    path('products/category/<int:category_id>',
         views.product_list,
         name='product_list'),
    path('product/<int:product_id>', views.product, name='product'),
]
