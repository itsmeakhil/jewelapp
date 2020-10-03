from django.db import models

from user.models import User
from utils.basemanager import BaseManager
from utils.basemodel import BaseModel


class ContactStatus(BaseModel):
    name = models.CharField(max_length=30, null=False, blank=False)
    description = models.CharField(max_length=50, null=True, blank=True)

    objects = BaseManager()

    def __str__(self):
        return self.name


class Customer(BaseModel):
    name = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True)
    phone_number = models.CharField(max_length=20, null=False, blank=True, unique=True)
    email = models.CharField(max_length=150, null=True, blank=True, unique=True)
    is_attended = models.BooleanField(default=False)

    objects = BaseManager()

    def __str__(self):
        return self.phone_number

    class Meta(object):
        unique_together = (('phone_number', 'email'),)


class CustomerStatusData(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    status = models.ForeignKey(ContactStatus, on_delete=models.DO_NOTHING)

    objects = BaseManager()

    def __str__(self):
        return self.customer.phone_number
