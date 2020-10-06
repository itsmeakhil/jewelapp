from rest_framework import serializers

from user import models as user_model


class UserTypeSerializer(serializers.ModelSerializer):
    """Serializer for adding user type"""

    class Meta:
        model = user_model.UserType
        fields = '__all__'
    #
    # def validate(self, data):
    #     """check user type exists"""
    #     if user_model.UserType.objects.does_exist_user_type(data['user_type']):
    #         raise serializers.ValidationError("User type already exists")
    #     return data


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user operations"""
    user_type_name = serializers.SerializerMethodField()
    branch_name = serializers.SerializerMethodField()
    company_name = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()

    class Meta:
        model = user_model.User
        fields = (
            'id', 'name', 'username', 'email', 'phone_number', 'key', 'user_type', 'user_type_name', 'is_admin',
            'branch', 'branch_name', 'company', 'company_name')
        read_only_fields = ('branch_name', 'company_name', 'user_type_name', 'company')

    def get_user_type_name(self, obj):
        return obj.user_type.user_type

    def get_branch_name(self, obj):
        return obj.branch.name

    def get_company_name(self, obj):
        return obj.branch.company.name

    def get_company(self, obj):
        return obj.branch.company.id

    def validate(self, data):
        """Conditions to check if phone number email or username already exists """
        if user_model.User.objects.does_exist_phone_number(data['phone_number']):
            raise serializers.ValidationError("Phone number already exists")
        return data


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer to update the user details"""

    class Meta:
        model = user_model.User
        fields = '__all__'


class UserAuthSerializer(serializers.Serializer):
    """Serializer for User Authentication"""
    employee_id = serializers.CharField()
    password = serializers.CharField()
