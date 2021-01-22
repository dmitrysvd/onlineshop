from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from .tasks import send_email_about_order
from cart.cart import Cart


def create_order(request):
    cart = Cart(request.session)
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
            send_email_about_order.delay(order.id)
            request.session['order_id'] = order.id
            return redirect('payment:process')
    else:
        form = OrderCreateForm()

    return render(request,
                  'orders/create_order.html',
                  {'cart': cart, 'form': form})


def order_created(request):
    return render(request,
                  'orders/order_created.html')
