from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser
from .managers import UserManager

class User(AbstractBaseUser):
    email = models.EmailField(max_length=255,unique=True)
    phone_number = models.CharField(max_length=255,unique=True)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()
    # The user how gonna registery 
    USERNAME_FIELD = 'phone_number'
    # in createsuper user which field shold be ask
    REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self) -> str:
        return self.email
    
    # for checking Does the user have specific permission
    def has_perm(self, perm, obj=None):
        # Simplest possible answer: Yes, always
        return True
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class OTP(models.Model):
    phone_number = models.CharField(max_length=11,unique=True)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created}'