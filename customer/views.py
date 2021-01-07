from rest_framework import viewsets
from rest_framework.views import APIView

from customer import service
from customer.models import CustomerFieldReport
from customer.serializers import CustomerFieldReportSerializer
from utils import responses as response, logger

service = service.CustomerService()


class UpdatePhoneNumberStatus(APIView):

    def post(self, request):
        try:
            return service.update_phone_status(data=request.data, user=request.user)
        except Exception as e:
            logger.error(f'Request -- Error : updating phone number status in to system {e}')
            return response.exception_500(e)


class UpdateCustomerStatus(APIView):

    def post(self, request):
        try:
            return service.update_service_Status(data=request.data, user=request.user)
        except Exception as e:
            logger.error(f'Request -- Error : updating customer status in to system {e}')
            return response.exception_500(e)


class AddCustomerRemarks(APIView):

    def post(self, request):
        try:
            return service.add_customer_remarks(data=request.data)
        except Exception as e:
            logger.error(f'Request -- Error : Adding Agents remarks in to system {e}')
            return response.exception_500(e)


class CustomerDetails(APIView):

    def get(self, request, pk):
        try:
            return service.get_customer_details(pk=pk)
        except Exception as e:
            logger.error(f'Request -- Error : Adding Agents remarks in to system {e}')
            return response.exception_500(e)

    def put(self, request, pk):
        try:
            return service.update_customer(pk=pk, data=request.data)
        except Exception as e:
            logger.error(f'Request -- Error : Adding Agents remarks in to system {e}')
            return response.exception_500(e)


class Customer(APIView):

    def get(self, request):
        try:
            return service.get_customer()
        except Exception as e:
            logger.error(f'Request -- Error : Getting customer details from system {e}')
            return response.exception_500(e)

    def post(self, request):
        try:
            return service.add_customer(data=request.data)
        except Exception as e:
            logger.error(f'Request -- Error : Adding Customer details in to system {e}')
            return response.exception_500(e)


class GetCustomersByUser(APIView):

    def get(self, request):
        try:
            return service.get_customers_by_assigned_user(request)
        except Exception as e:
            logger.error(f'Request -- Error : Getting customer details from system {e}')
            return response.exception_500(e)


class GetCustomersByAssignedUser(APIView):

    def get(self, request, pk):
        try:
            return service.get_customers_list_by_user(pk)
        except Exception as e:
            logger.error(f'Request -- Error : Getting customer details from system {e}')
            return response.exception_500(e)


class AssignCustomers(APIView):

    def post(self, request):
        try:
            return service.assign_customers(request.data)
        except Exception as e:
            logger.error(f'Request -- Error : Assigning customer details from system {e}')
            return response.exception_500(e)


class GetCustomersList(APIView):

    def get(self, request):
        try:
            return service.get_all_customers(request)
        except Exception as e:
            logger.error(f'Request -- Error : Getting customer list in to system {e}')
            return response.exception_500(e)


class FieldReportViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing field report.
    """
    queryset = CustomerFieldReport.objects.get_all_active()
    serializer_class = CustomerFieldReportSerializer

    def create(self, request, *args, **kwargs):
        return service.add_field_report(request.data)

    def update(self, request, pk, *args, **kwargs):
        return service.update_field_report(data=request.data, pk=pk)


class UpdatePhoneNumber(APIView):

    def put(self, request, pk):
        try:
            return service.update_phone_number(data=request.data, pk=pk)
        except Exception as e:
            logger.error(f'Request -- Error : updating phone number in to system {e}')
            return response.exception_500(e)
