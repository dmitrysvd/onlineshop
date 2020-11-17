from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product


def index(request):
    return redirect('categories')


def categories(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'onlinestore/categories.html', context=context)


def product_list(request, category_slug=None):
    category = None
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    context = {'category': category,
               'products': products}
    return render(request, 'onlinestore/product_list.html', context=context)


def product_detail(request, product_slug):
    product = get_object_or_404(Product,
                                slug=product_slug,
                                available=True)
    context = {'product': product}
    return render(request, 'onlinestore/product_info.html', context=context)


def shopcart(request):
    context = {}
    return render(request, 'onlinestore/shopcart.html', context=context)
