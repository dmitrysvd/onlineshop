from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product
from cart.forms import ItemQuantityUpdateForm
from cart.cart import Cart
import random


def main(request):
    try:
        sale_item = random.choice(
            Product.objects.filter(sale=True, available=True)
        )
    except IndexError:
        sale_item = None
    popular_products = Product.objects.order_by('-popularity')[:8]
    context = {'sale_item': sale_item,
               'popular_products': popular_products, }
    return render(request, 'onlinestore/main.html', context=context)


def product_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)

    # sorting
    sort_option = request.GET.get('sort')
    if sort_option == 'popularity':
        products = products.order_by('-popularity')
    elif sort_option == 'price':
        products = sorted(products, key=lambda p: p.current_price)
    else:
        products = products.order_by('-popularity')

    context = {'category': category,
               'products': products}
    return render(request, 'onlinestore/product_list.html', context=context)


def product_detail(request, product_id):
    product = get_object_or_404(Product,
                                pk=product_id)
    cart = Cart(request)
    product_is_in_cart = cart.contains(product)
    context = {'product': product,
               'is_in_cart': product_is_in_cart}
    return render(request, 'onlinestore/product_detail.html', context=context)
