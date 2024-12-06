from django.core.management import BaseCommand
from accounts.models import OTP
from datetime import datetime,timedelta 
from pytz import timezone


class Command(BaseCommand):
    help = "Remove all Otp code has expired"
    def handle(self, *args, **options) -> str | None:
        expired_time = datetime.now(tz=timezone('Asia/Tehran')) - timedelta(minutes=2)
        OTP.objects.filter(created__lt=expired_time).delete()
        self.stdout.write("All expired code had been deleted")