from django.db import models

from utils.basemanager import BaseManager
from utils.basemodel import BaseModel


class Company(BaseModel):
    name = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=False, blank=True)
    email = models.CharField(max_length=150, null=True, blank=True)

    objects = BaseManager()

    def __str__(self):
        return self.name


class Branch(BaseModel):
    name = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=False, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    objects = BaseManager()

    def __str__(self):
        return self.name
