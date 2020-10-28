from rest_framework import serializers

from customer.models import Customer, CustomerPhoneNumber, CustomerRemarks


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for adding Customers"""

    # group_name = serializers.SerializerMethodField()
    # area_name = serializers.SerializerMethodField()
    # number = serializers.SerializerMethodField()
    # remarks = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = '__all__'
        # ('id', 'name', 'group', 'area', 'area_name', 'group_name', 'address',
        #       'email', 'is_attended', 'number', 'remarks')
        # read_only_fields = ('group_name', 'area_name', 'number', 'remarks')

    #
    # def get_number(self, obj):
    #     data = AgentPhoneNumber.objects.get_by_filter(agent=obj.id)
    #     data = AgentPhoneNumberSerializer(data, many=True)
    #     return data.data
    #
    # def get_remarks(self, obj):
    #     data = AgentRemarks.objects.get_by_filter(agent=obj.id)
    #     data = AgentRemarksSerializer(data, many=True)
    #     return data.data


class CustomerPhoneNumberSerializer(serializers.ModelSerializer):
    """Serializer for adding Customer phone number"""

    class Meta:
        model = CustomerPhoneNumber
        fields = '__all__'


class CustomerRemarksSerializer(serializers.ModelSerializer):
    """Serializer for adding Customer Remarks"""

    class Meta:
        model = CustomerRemarks
        fields = '__all__'
