from utils import responses as response, constants, logger
from customer.models import Customer, CustomerStatusData, ContactStatus
from customer.serializers import CustomerSerializer


class CustomerServicetype:

    def get_customer(self, request):
        if Customer.objects.filter(is_attended=False).exists():
            customer = Customer.objects.get_by_filter(is_attended=False)[0]
            customer.is_attended = True
            customer.save()
            status = ContactStatus.objects.get(name="Attended")
            customer_service = CustomerStatusData.objects.create(customer=customer, user=request.user, status=status)
            serializer = CustomerSerializer(customer)
            logger.info('Get customer success')
            return response.get_success_200(' details loaded successfully', serializer.data)
        logger.error(' No Customer data found ')
        return response.get_success_message('No data found')

    def update_service_Status(self, data):
        customer_service = CustomerStatusData.objects.get(customer=data['customer'])
        if customer_service:
            status = ContactStatus.objects.get_by_id(data['status'])
            customer_service.status = status
            customer_service.save()
            return response.post_success('Updated Customer Service Status')
        return response.error_response_400('Error Updating status')
