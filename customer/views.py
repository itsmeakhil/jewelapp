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


class UpdateCustomerStatus(APIView):
    service = customer_service.CustomerServicetype()

    def post(self, request):
        try:
            return self.service.update_service_Status(data=request.data)
        except Exception as e:
            logger.error(f'Request -- Error : updating customer status in to system {e}')
            return response.exception_500(e)
