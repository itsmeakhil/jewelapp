from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from utils import responses as response, logger
from utils.utils import get_client_ip
from questions import service
from user.models import User


class GetQuestions(APIView):
    service = service.QuestionService()

    def get(self, request):
        """User Login function"""
        try:
            company = request.GET.get('company')
            ip = get_client_ip(request)
            return self.service.get_question(company)
        except Exception as e:
            logger.error(f'Request -- Error : Login in to system {e}')
            return response.exception_500(e)

