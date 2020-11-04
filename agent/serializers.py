from rest_framework import serializers

from agent.models import Agent, ContactStatus, AgentPhoneNumber, PhoneNumberStatus, AgentRemarks


class AgentSerializer(serializers.ModelSerializer):
    """Serializer for adding Agents"""
    group_name = serializers.SerializerMethodField()
    area_name = serializers.SerializerMethodField()
    number = serializers.SerializerMethodField()
    remarks = serializers.SerializerMethodField()

    class Meta:
        model = Agent
        fields = ('id', 'name', 'group', 'area', 'area_name', 'group_name', 'address',
                  'email', 'is_attended', 'is_assigned', 'number', 'remarks')
        read_only_fields = ('group_name', 'area_name', 'number', 'remarks')

    def get_group_name(self, obj):
        return obj.group.name

    def get_area_name(self, obj):
        return obj.area.name

    def get_number(self, obj):
        data = AgentPhoneNumber.objects.get_by_filter(agent=obj.id)
        data = AgentPhoneNumberSerializer(data, many=True)
        return data.data

    def get_remarks(self, obj):
        data = AgentRemarks.objects.get_by_filter(agent=obj.id)
        data = AgentRemarksSerializer(data, many=True)
        return data.data


class ContactStatusSerializer(serializers.ModelSerializer):
    """Serializer for adding Contact status"""

    class Meta:
        model = ContactStatus
        fields = '__all__'


class PhoneNumberStatusSerializer(serializers.ModelSerializer):
    """Serializer for adding Phone Number status"""

    class Meta:
        model = PhoneNumberStatus
        fields = '__all__'


class AgentPhoneNumberSerializer(serializers.ModelSerializer):
    """Serializer for adding Agent phone number"""
    class Meta:
        model = AgentPhoneNumber
        fields = '__all__'


class AgentRemarksSerializer(serializers.ModelSerializer):
    """Serializer for adding Agent Remarks"""

    class Meta:
        model = AgentRemarks
        fields = '__all__'
