from django.urls import path

from . import views

app_name = 'onlinestore'

urlpatterns = [
    path('', views.main, name='main'),
    path('products/<slug:category_slug>/',
         views.product_list,
         name='product_list'),
    path('product/<int:product_id>/',
         views.product_detail,
         name='product_detail'),
    path('search/<str:option>',
         views.search,
         name='search')
]
