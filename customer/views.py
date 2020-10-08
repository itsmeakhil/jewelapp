from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from utils import responses as response, logger
from utils.utils import get_client_ip
from customer import service as customer_service
from user.models import User


class GetCustomer(APIView):
    service = customer_service.CustomerServicetype()

    def get(self, request):
        """User Login function"""
        try:
            return self.service.get_customer(request)
        except Exception as e:
            logger.error(f'Request -- Error : Login in to system {e}')
            return response.exception_500(e)


class GetContactStatus(APIView):
    service = customer_service.CustomerServicetype()

    def get(self, request):
        """User Login function"""
        try:
            company = request.GET.get('company')
            return self.service.get_contact_status(company)
        except Exception as e:
            logger.error(f'Request -- Error : Login in to system {e}')
            return response.exception_500(e)


class UpdateCustomerStatus(APIView):
    service = customer_service.CustomerServicetype()

    def post(self, request):
        try:
            return self.service.update_service_Status(data=request.data, user=request.user)
        except Exception as e:
            logger.error(f'Request -- Error : updating customer status in to system {e}')
            return response.exception_500(e)


class AddQuestionAnswer(APIView):
    service = customer_service.CustomerServicetype()

    def post(self, request):
        try:
            return self.service.add_question_response(data=request.data.get('answer'))
        except Exception as e:
            logger.error(f'Request -- Error : Question answer in to system {e}')
            return response.exception_500(e)
