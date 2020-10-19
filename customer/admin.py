from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from customer.models import Customer, CustomerStatusData, ContactStatus, Group


class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer


@admin.register(Customer)
class CustomerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """
     Register the UserType class in django admin.
    """

    list_display = ('name', 'phone_number', 'mobile_number', 'phone_res', 'email', 'group')
    search_fields = ('name', 'phone_number')
    ordering = ('name',)
    list_filter = ('name', 'created_at', 'group',)
    exclude = ['is_delete', 'is_active']
    fieldsets = (
        (None, {
            'fields': ('name', 'phone_number', 'email', 'mobile_number', 'phone_res', 'is_attended', 'group', 'address')
        }),
    )



@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """
     Register the Group class in django admin.
    """

    list_display = ('id','name',)
    search_fields = ('name',)
    ordering = ('created_at',)
    list_filter = ('name', 'created_at',)
    exclude = ['is_delete', 'is_active']
    fieldsets = (
        (None, {
            'fields': ('name', 'company','description')
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
            'fields': ('name', 'description', 'company')
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
