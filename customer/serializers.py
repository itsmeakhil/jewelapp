from rest_framework import serializers

from customer.models import Customer, ContactStatus


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for adding Customer"""

    class Meta:
        model = Customer
        fields = '__all__'


class ContactStatusSerializer(serializers.ModelSerializer):
    """Serializer for adding Contact status"""

    class Meta:
        model = ContactStatus
        fields = '__all__'
