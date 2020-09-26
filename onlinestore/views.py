from django.shortcuts import render, redirect
from .models import Category, Product


def index(request):
    return redirect('categories')


def categories(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'onlinestore/categories.html', context=context)


def product_list(request, category_id):
    products = Product.objects.filter(category__id=category_id)
    context = {'products': products}
    return render(request, 'onlinestore/products.html', context=context)


def product(request, product_id):
    product = Product.objects.get(pk=product_id)
    context = {'product': product}
    return render(request, 'onlinestore/product.html', context=context)
