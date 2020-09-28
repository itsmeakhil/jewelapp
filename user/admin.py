from django.contrib import admin
from rest_framework.authtoken.models import Token

from user.models import UserType, User
from django.contrib.auth.models import Group

admin.site.unregister(Group)


# admin.site.unregister(Token)

@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    """
     Register the UserType class in django admin.
    """
    list_display = ('user_type', 'description')
    search_fields = ('user_type',)
    ordering = ('user_type',)
    exclude = ['is_delete', 'is_active']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
     Register the User class in django admin.
    """
    list_display = ('name', 'username', 'email', 'phone_number', 'user_type', 'branch')
    search_fields = ('name', 'username', 'email')
    list_filter = ('name', 'user_type', 'branch')
    ordering = ('name',)
    exclude = ['is_delete', 'is_active']
    fieldsets = (
        (None, {
            'fields': ('name', 'phone_number', 'email', 'password', 'username', 'user_type', 'branch')
        }),
    )
