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
    print(category_id)
    category = Category.objects.get(id=category_id)
    context = {'category': category.name,
               'products': products}
    return render(request, 'onlinestore/product_list.html', context=context)


def product(request, product_id):
    product = Product.objects.get(pk=product_id)
    context = {'product': product}
    return render(request, 'onlinestore/product_info.html', context=context)


def shopcart(request):
    context = {}
    return render(request, 'onlinestore/shopcart.html', context=context)
