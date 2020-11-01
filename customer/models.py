from django.db import models

from agent.models import Agent, PhoneNumberStatus
from utils.basemanager import BaseManager
from utils.basemodel import BaseModel


class Customer(BaseModel):
    application_no = models.CharField(max_length=10, null=True, blank=True)
    bride_name = models.CharField(max_length=100, null=True, blank=True)
    name_of_guardian = models.CharField(max_length=100, null=True, blank=True)
    house_name = models.CharField(max_length=100, null=True, blank=True)
    place = models.CharField(max_length=100, null=True, blank=True)
    post_office = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    marriage_date = models.DateTimeField(null=True, blank=True)
    agent = models.ForeignKey(Agent, on_delete=models.DO_NOTHING)

    objects = BaseManager()

    def __str__(self):
        return self.bride_name


class CustomerPhoneNumber(BaseModel):
    phone_number = models.BigIntegerField(null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.ForeignKey(PhoneNumberStatus, on_delete=models.DO_NOTHING)

    objects = BaseManager()

    def __str__(self):
        return self.customer.bride_name


class CustomerRemarks(BaseModel):
    remarks = models.TextField(null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, editable=False)

    objects = BaseManager()

    def __str__(self):
        return self.customer.bride_name
