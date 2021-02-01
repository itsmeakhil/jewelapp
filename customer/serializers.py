from rest_framework import serializers

from customer.models import Customer, CustomerPhoneNumber, CustomerRemarks, CustomerFieldReport, CustomerFieldAgent, \
    CustomerWithFieldReport


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
        fields = (
            'id', 'bride_name', 'name_of_guardian', 'name_of_father', 'name_of_mother', 'house_name', 'place', 'area',
            'area_name', 'post_office', 'district', 'marriage_date', 'number', 'remarks', 'agent')
        read_only_fields = ('area_name', 'number', 'remarks')

    def get_number(self, obj):
        data = CustomerPhoneNumber.objects.get_by_filter(customer=obj.id, status__is_invalid=False)
        data = CustomerPhoneNumberSerializer(data, many=True)
        return data.data

    def get_area_name(self, obj):
        return obj.area.name

    def get_remarks(self, obj):
        data = CustomerRemarks.objects.get_by_filter(customer=obj.id)
        data = CustomerRemarksGetSerializer(data, many=True)
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


class CustomerRemarksGetSerializer(serializers.ModelSerializer):
    """Serializer for getting Customer Remarks"""
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomerRemarks
        fields = ('id', 'remarks', 'customer', 'date', 'user', 'user_name')
        read_only_fields = ('user_name',)

    def get_user_name(self, obj):
        return obj.user.name


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
    customer = CustomerGetSerializer(read_only=True)

    class Meta:
        model = CustomerFieldAgent
        fields = ('user', 'customer')


class CustomerWithFieldReportGetSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = CustomerWithFieldReport
        fields = ('id', 'customer')
