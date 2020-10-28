from rest_framework.views import APIView

from customer import service
from utils import responses as response, logger


class UpdatePhoneNumberStatus(APIView):
    service = service.CustomerService()

    def post(self, request):
        try:
            return self.service.update_phone_status(data=request.data, user=request.user)
        except Exception as e:
            logger.error(f'Request -- Error : updating phone number status in to system {e}')
            return response.exception_500(e)


class AddCustomerRemarks(APIView):
    service = service.CustomerService()

    def post(self, request):
        try:
            return self.service.add_customer_remarks(data=request.data)
        except Exception as e:
            logger.error(f'Request -- Error : Adding Agents remarks in to system {e}')
            return response.exception_500(e)


class AddCustomer(APIView):
    service = service.CustomerService()

    def post(self, request):
        try:
            return self.service.add_customer(data=request.data)
        except Exception as e:
            logger.error(f'Request -- Error : Adding Customer details in to system {e}')
            return response.exception_500(e)
