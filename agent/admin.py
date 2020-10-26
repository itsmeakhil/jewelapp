from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from agent.models import Agent, AgentStatus, ContactStatus, Group, Area, AgentPhoneNumber, PhoneNumberStatus

admin.site.register(AgentPhoneNumber)
admin.site.register(PhoneNumberStatus)


@admin.register(Agent)
class AgentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """
     Register the UserType class in django admin.
    """

    list_display = ('name', 'address', 'email', 'group', 'area')
    search_fields = ('name',)
    ordering = ('name',)
    list_filter = ('name', 'created_at', 'group', 'area')
    exclude = ['is_delete', 'is_active']
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'is_attended', 'group', 'area', 'address')
        }),
    )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """
     Register the Group class in django admin.
    """

    list_display = ('id', 'name',)
    search_fields = ('name',)
    ordering = ('created_at',)
    list_filter = ('name', 'created_at',)
    exclude = ['is_delete', 'is_active']
    fieldsets = (
        (None, {
            'fields': ('name', 'company', 'description')
        }),
    )


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    """
     Register the Area class in django admin.
    """

    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('created_at',)
    list_filter = ('name', 'created_at',)
    exclude = ['is_delete', 'is_active']
    fieldsets = (
        (None, {
            'fields': ('name', 'company')
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


@admin.register(AgentStatus)
class AgentStatusAdmin(admin.ModelAdmin):
    """
     Register the CustomerService class in django admin.
    """

    list_display = ('agent', 'user', 'status')
    search_fields = ('agent', 'user',)
    ordering = ('created_at',)
    list_filter = ('agent', 'user', 'status', 'created_at',)
    exclude = ['is_delete', 'is_active']
    fieldsets = (
        (None, {
            'fields': ('agent', 'user', 'status')
        }),
    )
