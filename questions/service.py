from questions.models import Question
from questions.serializers import GetQuestionSerializer
from utils import responses as response, logger


class QuestionService:

    def get_question(self):
        question_exists = Question.objects.filter().exists()
        if question_exists:
            question = Question.objects.get_all_active()
            serializer = GetQuestionSerializer(question, many=True)
            logger.info('GET Questions success')
            return response.get_success_200('Questions  loaded successfully', serializer.data)
        logger.error(' No Customer data found ')
        return response.get_success_message('No questions found')
