from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product
from cart.forms import ItemQuantityUpdateForm
from cart.cart import Cart


def main(request):
    context = {}
    return render(request, 'onlinestore/main.html', context=context)


def product_list(request, category_slug=None):
    category = None
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    context = {'category': category,
               'products': products}
    return render(request, 'onlinestore/product_list.html', context=context)


def product_detail(request, product_id):
    product = get_object_or_404(Product,
                                pk=product_id,
                                available=True)
    cart = Cart(request)
    product_is_in_cart = cart.contains(product)
    context = {'product': product,
               'is_in_cart': product_is_in_cart}
    return render(request, 'onlinestore/product_detail.html', context=context)
