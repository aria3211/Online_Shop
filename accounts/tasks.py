from celery import shared_task
from datetime import datetime,timedelta 
from pytz import timezone
from accounts.models import OTP




@shared_task
def remove_expire_codes_task():
    expired_time = datetime.now(tz=timezone('Asia/Tehran')) - timedelta(minutes=2)
    OTP.objects.filter(created__lt=expired_time).delete()
