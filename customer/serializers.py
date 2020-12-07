from rest_framework import serializers

from customer.models import Customer, CustomerPhoneNumber, CustomerRemarks, CustomerFieldReport, CustomerFieldAgent


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for adding Customers"""

    class Meta:
        model = Customer
        fields = '__all__'


class CustomerGetSerializer(serializers.ModelSerializer):
    """Serializer for getting Customers"""
    area_name = serializers.SerializerMethodField()
    number = serializers.SerializerMethodField()
    remarks = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ('id','bride_name', 'name_of_guardian', 'house_name', 'place', 'area', 'area_name', 'post_office',
                  'district', 'marriage_date', 'number', 'remarks')
        read_only_fields = ('area_name', 'number', 'remarks')

    def get_number(self, obj):
        data = CustomerPhoneNumber.objects.get_by_filter(customer=obj.id, status__is_invalid=False)
        data = CustomerPhoneNumberSerializer(data, many=True)
        return data.data

    def get_area_name(self, obj):
        return obj.area.name

    def get_remarks(self, obj):
        data = CustomerRemarks.objects.get_by_filter(customer=obj.id)
        data = CustomerRemarksSerializer(data, many=True)
        return data.data


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


class CustomerFieldReportSerializer(serializers.ModelSerializer):
    """Serializer for adding Customer Remarks"""

    class Meta:
        model = CustomerFieldReport
        fields = '__all__'


class CustomerFieldReportGetSerializer(serializers.ModelSerializer):
    """Serializer for getting Customer field report"""

    class Meta:
        model = CustomerFieldReport
        fields = '__all__'


class CustomerFieldAgentReportSerializer(serializers.ModelSerializer):
    """Serializer for getting Customer agent assigned"""

    class Meta:
        model = CustomerFieldAgent
        fields = '__all__'


class CustomerFieldAgentGetReportSerializer(serializers.ModelSerializer):
    """Serializer for getting Customer Remarks"""
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = CustomerFieldAgent
        fields = ('user', 'customer')
