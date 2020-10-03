from rest_framework import serializers

from company.models import Company, Branch


class CompanySerializer(serializers.ModelSerializer):
    """Serializer for adding Company type"""

    class Meta:
        model = Company
        fields = '__all__'
    #
    # def validate(self, data):
    #     """check user type exists"""
    #     if user_model.UserType.objects.does_exist_user_type(data['user_type']):
    #         raise serializers.ValidationError("User type already exists")
    #     return data


class BranchSerializer(serializers.ModelSerializer):
    """Serializer for Branch operations"""


    class Meta:
        model =Branch
        fields = '__all__'

    # def validate(self, data):
    #     """Conditions to check if phone number email or username already exists """
    #     if user_model.User.objects.does_exist_phone_number(data['phone_number']):
    #         raise serializers.ValidationError("Phone number already exists")
    #     return data

