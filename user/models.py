from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.hashers import PBKDF2PasswordHasher

from company.models import Branch
from utils.basemodel import BaseModel
from user.manager import UserManager, UserTypeManager
from passlib.hash import pbkdf2_sha256

hasher = PBKDF2PasswordHasher()


# Create your models here.
class UserType(BaseModel):
    user_type = models.CharField(max_length=30, null=False, blank=False)
    description = models.CharField(max_length=50, null=True, blank=True)

    objects = UserTypeManager()

    def __str__(self):
        return self.user_type


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=False, blank=True)
    password = models.CharField(max_length=150, null=True, blank=True)
    key = models.CharField(max_length=100, blank=True, default='')
    push_notification_key = models.TextField(default=' ', null=True, blank=True)
    user_type = models.ForeignKey(UserType, null=True, blank=True, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username
    #
    # def save(self, *args, **kwargs):
    #     if len(self.password) < 20:
    #         self.password = hasher.encode(password=self.password, salt='salt', iterations=50000)
    #         return super().save(*args, **kwargs)

    # .sa
    # def authenticate_otp(self, otp):
    #     """ This method authenticates the given otp """
    #     try:
    #         provided_otp = otp
    #     except:
    #         return False
    #     # Here we are using Time Based OTP. The interval is 60 seconds.
    #     # otp must be provided within this interval or it's invalid
    #     time_otp = pyotp.TOTP(self.key, interval=1000)
    #     return time_otp.verify(provided_otp)
