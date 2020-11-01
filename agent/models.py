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


class PhoneNumberStatus(BaseModel):
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


class Area(BaseModel):
    name = models.CharField(max_length=50, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    objects = BaseManager()

    def __str__(self):
        return self.name


class Agent(BaseModel):
    name = models.CharField(max_length=50, null=True, blank=True)
    code = models.CharField(max_length=50, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, null=True, default=1)
    area = models.ForeignKey(Area, on_delete=models.DO_NOTHING, null=True)
    address = models.TextField(null=True, blank=True)
    email = models.CharField(max_length=150, null=True, blank=True)
    is_attended = models.BooleanField(default=False)
    is_assigned = models.BooleanField(default=False)
    objects = BaseManager()

    def __str__(self):
        return self.name


class AgentPhoneNumber(BaseModel):
    phone_number = models.BigIntegerField(null=True, blank=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    status = models.ForeignKey(PhoneNumberStatus, on_delete=models.DO_NOTHING)

    objects = BaseManager()

    def __str__(self):
        return self.agent.name


class AgentRemarks(BaseModel):
    remarks = models.TextField(null=True, blank=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, editable=False)

    objects = BaseManager()

    def __str__(self):
        return self.agent.name


class AgentStatus(BaseModel):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    status = models.ForeignKey(ContactStatus, on_delete=models.DO_NOTHING)

    objects = BaseManager()

    def __str__(self):
        return self.agent.name
