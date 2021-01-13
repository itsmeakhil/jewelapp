from django.contrib import admin

from customer.models import Customer, CustomerPhoneNumber, CustomerRemarks, CustomerFieldReport, CustomerStatus, \
    CustomerFieldAgent, CustomerWithFieldReport

admin.site.register(Customer)
admin.site.register(CustomerPhoneNumber)
admin.site.register(CustomerRemarks)
admin.site.register(CustomerFieldReport)
admin.site.register(CustomerStatus)
admin.site.register(CustomerFieldAgent)


@admin.register(CustomerWithFieldReport)
class CustomerWithFieldReportAdmin(admin.ModelAdmin):
    list_display = ('customer', 'user')
    search_fields = ('customer__bride_name',)
    ordering = ('last_call_date',)
    list_filter = ('customer', 'user',)
    exclude = ['is_active']
    # fieldsets = (
    #     (None, {
    #         'fields': ('name', 'address', 'phone_number', 'email')
    #     }),
    # )
