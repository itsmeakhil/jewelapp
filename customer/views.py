from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from customer import service as customer_service
from utils import responses as response, logger


class GetCustomer(APIView):
    service = customer_service.CustomerServicetype()

    def get(self, request):
        """User Login function"""
        try:
            return self.service.get_customer(request)
        except Exception as e:
            logger.error(f'Request -- Error : Login in to system {e}')
            return response.exception_500(e)


@permission_classes((AllowAny,))
class GetContactStatus(APIView):
    service = customer_service.CustomerServicetype()

    def get(self, request):
        """User Login function"""
        try:
            return self.service.get_contact_status()
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
            return self.service.add_answer(data=request.data)
        except Exception as e:
            logger.error(f'Request -- Error : Question answer in to system {e}')
            return response.exception_500(e)


@permission_classes((AllowAny,))
class AddBulkCustomers(APIView):
    service = customer_service.CustomerServicetype()

    def post(self, request):
        try:
            return self.service.add_customers(request)
        except Exception as e:
            logger.error(f'Request -- Error : Question answer in to system {e}')
            return response.exception_500(e)
