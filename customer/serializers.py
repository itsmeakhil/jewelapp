from rest_framework import serializers

from customer.models import Customer



class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for adding user type"""

    class Meta:
        model = Customer
        fields = '__all__'
