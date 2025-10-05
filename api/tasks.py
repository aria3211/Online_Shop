from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


# send order confirmation email
@shared_task()
def send_order_conf_email(order_id,user_email):
    subject = 'Welcome to Our Service!'
    message = f"Your order with ID {order_id} has been receviing and its being processed. "
    
    send_mail(subject, message,settings.DEFAULT_FROM_EMAIL, [user_email])
    print(f"Welcome email sent to {user_email}")