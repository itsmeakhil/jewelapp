from django.contrib import admin

from customer.models import Customer, CustomerPhoneNumber, CustomerRemarks, CustomerFieldReport, CustomerStatus, \
    CustomerFieldAgent, CustomerWithFieldReport

admin.site.register(Customer)
admin.site.register(CustomerPhoneNumber)
admin.site.register(CustomerRemarks)
admin.site.register(CustomerFieldReport)
admin.site.register(CustomerStatus)
admin.site.register(CustomerFieldAgent)
admin.site.register(CustomerWithFieldReport)
