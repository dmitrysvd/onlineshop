from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from .cart import Cart
from onlinestore.models import Product
from .forms import CartUpdateProductForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product)
    return redirect('cart:cart_detail')


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartUpdateProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.update(product=product,
                    quantity=cd['quantity'])
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    items = [item for item in cart]
    for item in items:
        item['update_quantity_form'] = CartUpdateProductForm(
            initial={'quantity': item['quantity']})
    context = {'cart': cart,
               'items': items}
    return render(request, 'cart/cart_detail.html', context)
