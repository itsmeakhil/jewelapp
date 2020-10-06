from rest_framework import serializers

from customer.models import Customer
from questions.models import Question, QuestionOption


class GetQuestionSerializer(serializers.ModelSerializer):
    """Serializer for adding Question"""
    options = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ('id', 'content', 'options')
        read_only_fields = ('options',)

    def get_options(self, obj):
        data = QuestionOption.objects.filter(question=obj.id).exists()
        if data:
            data = QuestionOptionSerializer(data, many=True)
            return data.data
        return ''


class QuestionOptionSerializer(serializers.ModelSerializer):
    """Serializer for adding QuestionOption"""

    class Meta:
        model = QuestionOption
        fields = '__all__'
