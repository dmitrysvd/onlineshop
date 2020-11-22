from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


def create_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            context = {'cart': cart, 'form': form}
            return render(request,
                          'orders/order_created.html',
                          context)
    else:
        form = OrderCreateForm()
        context = {'cart': cart, 'form': form}
        return render(request,
                      'orders/create_order.html',
                      context)
