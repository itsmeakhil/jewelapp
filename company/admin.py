from django.contrib import admin

# Register your models here.
from company.models import Branch, Company


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    """
     Register the UserType class in django admin.
    """

    list_display = ('name', 'address', 'phone_number', 'company')
    search_fields = ('name', 'phone_number')
    ordering = ('created_at',)
    list_filter = ('name', 'created_at',)
    exclude = ['is_delete', 'is_active']
    fieldsets = (
        (None, {
            'fields': ('name', 'address', 'phone_number', 'company')
        }),
    )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """
     Register the UserType class in django admin.
    """

    list_display = ('name', 'address', 'phone_number', 'email')
    search_fields = ('name', 'phone_number')
    ordering = ('created_at',)
    list_filter = ('name', 'created_at',)
    exclude = ['is_delete', 'is_active']
    fieldsets = (
        (None, {
            'fields': ('name', 'address', 'phone_number', 'email')
        }),
    )
