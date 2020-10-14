from rest_framework import serializers

from customer.models import Customer, ContactStatus


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for adding Customer"""
    group_name = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ('id', 'name', 'group', 'group_name', 'address', 'phone_number', 'email', 'is_attended')
        read_only_fields = ('group_name',)

    def get_group_name(self, obj):
        return obj.group.name


class ContactStatusSerializer(serializers.ModelSerializer):
    """Serializer for adding Contact status"""

    class Meta:
        model = ContactStatus
        fields = '__all__'
