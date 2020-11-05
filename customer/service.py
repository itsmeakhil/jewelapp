from django.db import transaction

from agent.models import ContactStatus, PhoneNumberStatus
from agent.serializers import ContactStatusSerializer
from customer.models import CustomerPhoneNumber, CustomerRemarks
from customer.serializers import CustomerRemarksSerializer, CustomerSerializer
from utils import responses as response, logger, constants


class CustomerService:
    # def get_customer(self, request):
    #     if Agent.objects.filter(is_attended=False).exists():
    #         agent = Agent.objects.get_by_filter(is_attended=False)[0]
    #         serializer = AgentSerializer(agent)
    #         logger.info('Get agent success')
    #         return response.get_success_200('Customer details loaded successfully', serializer.data)
    #     logger.error(' No Customer data found ')
    #     return response.get_success_message('No data found')

    # def update_service_Status(self, data, user):
    #     agent_status_exists = AgentStatus.objects.filter(agent=data['agent']).exists()
    #     status = ContactStatus.objects.get_by_id(data['status'])
    #     agent = Agent.objects.get_by_id(data['agent'])
    #     if agent_status_exists:
    #         agent_status = AgentStatus.objects.get(agent=data['agent'])
    #         status = ContactStatus.objects.get_by_id(data['status'])
    #         agent_status.status = status
    #         agent_status.user = user
    #         agent_status.save()
    #         agent.is_attended = True
    #         agent.save()
    #         return response.put_success_message('Updated Customer Service Status')
    #     AgentStatus.objects.create(agent=agent, user=user, status=status)
    #     return response.post_success('Added Customer Status Data')

    def get_contact_status(self):
        contact_status = ContactStatus.objects.get_all_active()
        serializer = ContactStatusSerializer(contact_status, many=True)
        logger.info('GET Contact status success')
        return response.get_success_200('Contact status loaded successfully', serializer.data)

    def update_phone_status(self, data, user):
        phone_exists = CustomerPhoneNumber.objects.filter(phone_number=data['phone_number']).exists()
        if phone_exists:
            status = PhoneNumberStatus.objects.get(data['status'])
            phone = CustomerPhoneNumber.objects.get(phone_number=data['phone_number'])
            phone.status = status
            phone.save()
            return response.put_success_message('Updated Customer Phone Number')
        return response.error_response_400('Unable to find the Phone number ')

    def add_customer(self, data):
        with transaction.atomic():
            print(data)
            serializer = CustomerSerializer(data=data)
            print(serializer.is_valid())
            if serializer.is_valid():
                print('here')
                customer = serializer.save()
                print(customer)
                status = PhoneNumberStatus.objects.get(name=constants.ACTIVE)
                if data['remarks']:
                    CustomerRemarks.objects.create(customer=customer, remarks=data['remarks'])
                if data['phone_number1']:
                    if not CustomerPhoneNumber.objects.get_by_filter(phone_number=int(data['phone_number1'])).exists():
                        CustomerPhoneNumber.objects.create(customer=customer, phone_number=int(data['phone_number1']),
                                                           status=status)
                if data['phone_number2']:
                    if not CustomerPhoneNumber.objects.get_by_filter(phone_number=int(data['phone_number2'])).exists():
                        CustomerPhoneNumber.objects.create(customer=customer, phone_number=int(data['phone_number2']),
                                                           status=status)
                if data['phone_number3']:
                    if not CustomerPhoneNumber.objects.get_by_filter(phone_number=int(data['phone_number3'])).exists():
                        CustomerPhoneNumber.objects.create(customer=customer, phone_number=int(data['phone_number3']),
                                                           status=status)

                return response.get_success_200('Customer Details added successfully', serializer.data)
            return response.serializer_error_400(serializer)

    def add_customer_remarks(self, data):
        with transaction.atomic():
            serializer = CustomerRemarksSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return response.post_success_201('Successfully added Remarks ', serializer.data)
            return response.serializer_error_400(serializer)
