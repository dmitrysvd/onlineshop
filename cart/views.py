from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from .cart import Cart
from onlinestore.models import Product


@require_POST
def cart_add(request, product_id):
    cart = Cart(request.session)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product)
    return redirect('cart:cart_detail')


@require_POST
def cart_update(request, product_id):
    cart = Cart(request.session)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST['quantity'])
    if quantity > 0:
        cart.update(product=product,
                    quantity=quantity)
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request.session)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request.session)
    items = [item for item in cart]
    context = {'cart': cart,
               'items': items}
    return render(request, 'cart/cart_detail.html', context)
