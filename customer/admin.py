from django.contrib import admin
from customer.models import Customer, CustomerStatusData, ContactStatus
from import_export import resources

from import_export.admin import ImportExportModelAdmin


class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer


@admin.register(Customer)
class CustomerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """
     Register the UserType class in django admin.
    """

    list_display = ('name', 'phone_number', 'email')
    search_fields = ('name', 'phone_number')
    ordering = ('created_at',)
    list_filter = ('name', 'created_at',)
    exclude = ['is_delete', 'is_active']
    fieldsets = (
        (None, {
            'fields': ('name', 'phone_number', 'email', 'is_attended')
        }),
    )


@admin.register(ContactStatus)
class ContactStatusAdmin(admin.ModelAdmin):
    """
     Register the UserType class in django admin.
    """

    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('created_at',)
    list_filter = ('name', 'created_at',)
    exclude = ['is_delete', 'is_active']
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
    )


@admin.register(CustomerStatusData)
class CustomerServiceAdmin(admin.ModelAdmin):
    """
     Register the CustomerService class in django admin.
    """

    list_display = ('customer', 'user', 'status')
    search_fields = ('customer', 'user',)
    ordering = ('created_at',)
    list_filter = ('customer', 'user', 'status', 'created_at',)
    exclude = ['is_delete', 'is_active']
    fieldsets = (
        (None, {
            'fields': ('customer', 'user', 'status')
        }),
    )
