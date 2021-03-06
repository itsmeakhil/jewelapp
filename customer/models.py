from django.db import models

from company.models import Branch, Company
from user.models import User
from utils.basemanager import BaseManager
from utils.basemodel import BaseModel


class ContactStatus(BaseModel):
    name = models.CharField(max_length=30, null=False, blank=False)
    description = models.CharField(max_length=50, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    objects = BaseManager()

    def __str__(self):
        return self.name


class Group(BaseModel):
    name = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    objects = BaseManager()

    def __str__(self):
        return self.name


class Customer(BaseModel):
    name = models.CharField(max_length=50, null=True, blank=True)
    code = models.CharField(max_length=50, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, null=True, default=1)
    address = models.TextField(null=True, blank=True)
    phone_number = models.BigIntegerField(null=False, blank=True)
    phone_res = models.CharField(max_length=20, null=True, blank=True)
    mobile_number = models.CharField(max_length=20, null=True, blank=True, )
    email = models.CharField(max_length=150, null=True, blank=True)
    is_attended = models.BooleanField(default=False)
    assigned_to = models.BooleanField(default=False)
    objects = BaseManager()

    def __str__(self):
        return self.name


class CustomerStatusData(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    status = models.ForeignKey(ContactStatus, on_delete=models.DO_NOTHING)

    objects = BaseManager()

    def __str__(self):
        return self.customer.phone_number
