from django.db import models

from agent.models import Agent, PhoneNumberStatus, Area, ContactStatus
from user.models import User
from utils.basemanager import BaseManager
from utils.basemodel import BaseModel

finance_bg = ((1, "1"), (2, "2"), (3, "3"))
customer_field_agent_status = ((1, "Open"), (2, "Updated"))


class Customer(BaseModel):
    bride_name = models.CharField(max_length=100, null=True, blank=True)
    name_of_guardian = models.CharField(max_length=100, null=True, blank=True)
    house_name = models.CharField(max_length=100, null=True, blank=True)
    name_of_father = models.CharField(max_length=100, null=True, blank=True)
    name_of_mother = models.CharField(max_length=100, null=True, blank=True)
    place = models.CharField(max_length=100, null=True, blank=True)
    area = models.ForeignKey(Area, on_delete=models.DO_NOTHING)
    post_office = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    marriage_date = models.DateField(null=True, blank=True)
    agent = models.ForeignKey(Agent, on_delete=models.DO_NOTHING)
    is_attended = models.BooleanField(default=False)
    is_assigned = models.BooleanField(default=False)

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
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1)
    objects = BaseManager()

    def __str__(self):
        return self.customer.bride_name


class CustomerFieldReport(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    marriage_date = models.DateField(null=True, blank=True)
    financial_bg = models.IntegerField(choices=finance_bg, default=1)
    gold_amt = models.CharField(max_length=10, null=True, blank=True)
    marriage_set = models.CharField(max_length=10, null=True, blank=True)
    is_exchanging = models.BooleanField(default=False, null=True, blank=True)
    is_exchanging_old = models.BooleanField(default=False, null=True, blank=True)
    gold_amt_exchanging = models.CharField(max_length=10, null=True, blank=True)
    is_taking_emi = models.BooleanField(default=False, null=True, blank=True)
    duration_of_loan = models.IntegerField(null=True, blank=True, default=0)
    number_of_emi = models.IntegerField(null=True, blank=True, default=0)
    is_advance_booking = models.BooleanField(default=False, null=True, blank=True)
    token_advance = models.CharField(max_length=10, null=True, blank=True)
    rate_at_booking = models.CharField(max_length=10, null=True, blank=True)
    image_1 = models.ImageField(upload_to='field_image/', null=True, blank=True)
    image_2 = models.ImageField(upload_to='field_image/', null=True, blank=True)
    image_3 = models.ImageField(upload_to='field_image/', null=True, blank=True)
    is_another_jeweller_came = models.BooleanField(default=False)
    is_advanced_in_other = models.BooleanField(default=False)
    amount_advanced_in_other = models.CharField(max_length=10, null=True, blank=True)
    know_any_new_party = models.BooleanField(default=False)
    no_of_party = models.IntegerField(null=True, blank=True, default=0)
    lat = models.CharField(max_length=30, null=True, blank=True)
    lon = models.CharField(max_length=30, null=True, blank=True)
    phone_number1 = models.CharField(max_length=30, null=True, blank=True)
    phone_number2 = models.CharField(max_length=30, null=True, blank=True)
    phone_number3 = models.CharField(max_length=30, null=True, blank=True)

    is_assigned = models.BooleanField(default=False)

    objects = BaseManager()

    def __str__(self):
        return self.customer.bride_name


class CustomerStatus(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    status = models.ForeignKey(ContactStatus, on_delete=models.DO_NOTHING)

    objects = BaseManager()

    def __str__(self):
        return self.customer.bride_name


class CustomerFieldAgent(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    status = models.IntegerField(choices=customer_field_agent_status, default=1)

    objects = BaseManager()

    def __str__(self):
        return self.customer.bride_name


class CustomerWithFieldReport(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    last_call_date = models.DateTimeField(null=True, blank=True, auto_now=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)

    objects = BaseManager()

    def __str__(self):
        return self.customer.bride_name
