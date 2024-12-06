from celery import shared_task
from django.core.mail import send_mail
from orders.models import Order
from accounts.models import User





@shared_task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order_id}'
    message = (
        f'Dear {order.user},\n\n'
        f'You have successfully placed an order.'
        f'Your order ID is {order.id}.'
    )
    mail_sent = send_mail(subject,message,'aryapoint1@gmail.com',[User.email])
    return mail_sent
