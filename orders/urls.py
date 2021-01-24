from orders.views import order_created
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create_order/', views.create_order, name='create_order'),
    path('created', views.order_created, name='order_created'),
    path('admin/order/<int:order_id>/',
         views.admin_order_detail,
         name='admin_order_detail'),
]
