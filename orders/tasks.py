from django.core.mail import send_mail
from .models import Order
from celery import shared_task


@shared_task
def send_email_about_order(order_id):
    order = Order.objects.get(id=order_id)
    print('XXX', order_id)
    subject = f'Order No. {order.id}'
    message = 'Your order has been successfully issued'
    mail_sent = send_mail(subject=subject,
                          message=message,
                          from_email='admin@onlinestore.com',
                          recipient_list=[order.email])
    return mail_sent
