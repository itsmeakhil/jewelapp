from rest_framework import serializers

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
            options = QuestionOption.objects.get_by_filter(question=obj.id)
            data = QuestionOptionSerializer(options, many=True)
            return data.data
        return ''


class QuestionOptionSerializer(serializers.ModelSerializer):
    """Serializer for adding QuestionOption"""

    class Meta:
        model = QuestionOption
        fields = '__all__'
