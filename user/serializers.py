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

    class Meta:
        model = user_model.User
        fields = (
            'id', 'name', 'username', 'email', 'phone_number', 'key', 'user_type', 'is_admin', 'branch', 'branch_name',
            'company_name', 'user_type_name')
        read_only_fields = ('branch_name', 'company_name', 'user_type_name',)

    def get_user_type_name(self, obj):
        print(obj.user_type.user_type)
        if obj.user_type.user_type:
            return obj.user_type.user_type
        return None

    def get_branch_name(self, obj):
        if obj.branch.name:
            print(obj.branch.name)
            return obj.branch.name
        return None

    def get_company_name(self, obj):
        if obj.branch.company.name:
            print(obj.branch.company.name)
            return obj.branch.company.name
        return None

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
