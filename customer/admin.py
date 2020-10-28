from django.contrib import admin

# Register your models here.
from customer.models import Customer, CustomerPhoneNumber, CustomerRemarks

admin.site.register(Customer)
admin.site.register(CustomerPhoneNumber)
admin.site.register(CustomerRemarks)
