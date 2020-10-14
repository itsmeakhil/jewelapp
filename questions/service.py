from questions.models import Question
from utils import responses as response, constants, logger
from customer.models import Customer, CustomerStatusData, ContactStatus
from questions.serializers import GetQuestionSerializer, QuestionOptionSerializer


class QuestionService:

    def get_question(self, company):
        if Question.objects.filter(company=company).exists():
            question = Question.objects.get_by_filter(company=company)
            serializer = GetQuestionSerializer(question, many=True)
            logger.info('GET Questions success')
            return response.get_success_200('Questions  loaded successfully', serializer.data)
        logger.error(' No Customer data found ')
        return response.get_success_message('No questions found')
