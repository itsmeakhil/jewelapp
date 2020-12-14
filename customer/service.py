from django.db import transaction
from django.db.models import Q

from agent.models import ContactStatus, PhoneNumberStatus
from customer.models import CustomerPhoneNumber, CustomerRemarks, CustomerFieldReport, Customer, CustomerStatus, \
    CustomerFieldAgent
from customer.serializers import CustomerRemarksSerializer, CustomerSerializer, CustomerGetSerializer, \
    CustomerFieldAgentGetReportSerializer, CustomerFieldReportGetSerializer, CustomerFieldReportSerializer, \
    CustomerFieldAgentReportSerializer
from utils import responses as response, logger, constants


class CustomerService:
    def get_customer(self):
        if Customer.objects.filter(is_attended=False).exists():
            customer = Customer.objects.get_by_filter(is_attended=False)[0]
            if CustomerFieldReport.objects.get_by_filter(customer=customer).exists():
                field_report = CustomerFieldReport.objects.get_by_filter(customer=customer)[0]
                field_report_serializer = CustomerFieldReportGetSerializer(field_report)
                serializer = CustomerGetSerializer(customer)
                customer.is_attended = True
                customer.save()
                data = {
                    "customer": serializer.data,
                    "field_report": field_report_serializer.data
                }
                logger.info('Get agent success')
                return response.get_success_200('Customer details loaded successfully', data)
        logger.error(' No Customer data found ')
        return response.get_success_message('No data found')

    def get_all_customers(self, request):
        customer = Customer.objects.get_by_filter(is_assigned=False)
        if request.GET.get('area'):
            customer = customer.filter(area=request.GET.get('area'))
        serializer = CustomerSerializer(customer, many=True)
        return response.get_success_200('Customer list loaded successfully', serializer.data)

    def update_service_Status(self, data, user):
        customer_status_exists = CustomerStatus.objects.filter(customer=data['customer']).exists()
        status = ContactStatus.objects.get_by_id(data['status'])
        customer = Customer.objects.get_by_id(data['customer'])
        if customer_status_exists:
            customer_status = CustomerStatus.objects.get(customer=data['customer'])
            status = ContactStatus.objects.get_by_id(data['status'])
            customer_status.status = status
            customer_status.user = user
            customer_status.save()
            customer.is_attended = True
            customer.save()
            return response.put_success_message('Updated Customer Service Status')
        CustomerStatus.objects.create(customer=customer, user=user, status=status)
        return response.post_success('Added Customer Status Data')

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
            serializer = CustomerSerializer(data=data)
            if serializer.is_valid():
                customer = serializer.save()
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

    def get_customers_by_assigned_user(self, request):
        customers = CustomerFieldAgent.objects.get_by_filter(user=request.user.id, status=1)
        customers = customers.order_by('created_at')
        if request.GET.get('q'):
            queryset = (Q(customer__bride_name__icontains=request.GET.get('q'))
                        | Q(customer__name_of_guardian__icontains=request.GET.get('q')))
            customers = customers.filter(queryset)
        customers_data = CustomerFieldAgentGetReportSerializer(customers, many=True)
        return response.get_success_200('Customers list loaded successfully', customers_data.data)

    def get_customers_list_by_user(self, user):
        customers = CustomerFieldAgent.objects.get_by_filter(user=user)
        customers = customers.order_by('created_at')
        customers_data = CustomerFieldAgentGetReportSerializer(customers, many=True)
        return response.get_success_200('Customers list loaded successfully', customers_data.data)

    def assign_customers(self, data):
        if data['customers'] and data['user']:
            for i in data['customers']:
                if not CustomerFieldAgent.objects.filter(customer=i).exists():
                    in_data = {"customer": i, "user": data['user']}
                    serializer = CustomerFieldAgentReportSerializer(data=in_data)
                    if serializer.is_valid():
                        print(data['customers'], data['user'])
                        serializer.save()
                        print(i)
                        customer = Customer.objects.get_by_id(i)
                        print(customer)
                        customer.is_assigned = True
                        customer.save()
            return response.post_success('Customers assigned successfully')
        return response.error_response_400('Entered data format is incorrect ')

    def add_field_report(self, data):
        with transaction.atomic():
            if data:
                if not CustomerFieldReport.objects.get_by_filter(customer=data['customer']).exists():
                    serialized_data = CustomerFieldReportSerializer(data=data)
                    if serialized_data.is_valid():
                        if CustomerFieldAgent.objects.get_by_filter(customer=data['customer']).exists():
                            cus_field_agent_data = CustomerFieldAgent.objects.get(customer=data['customer'])
                            cus_field_agent_data.status = 2,
                            serialized_data.save()
                            return response.post_success_201('Field Report added successfully', serialized_data.data)
                        return response.error_response_400('The customer is not assigned for field agent')
                    return response.serializer_error_400(serialized_data)
                return response.error_response_400('Field report for the customer already exists')
            return response.error_response_400('Invalid data format')

    def update_field_report(self, data, pk):
        with transaction.atomic():
            if data:
                if CustomerFieldReport.objects.get_by_id(pk):
                    field_data = CustomerFieldReport.objects.get_by_id(pk)
                    serialized_data = CustomerFieldReportSerializer(field_data, data=data)
                    if serialized_data.is_valid():
                        serialized_data.save()
                        return response.post_success_201('Field Report added successfully', serialized_data.data)
                    return response.serializer_error_400(serialized_data)
                return response.error_response_400('Field report for the customer not found ')
            return response.error_response_400('Invalid data format ')

    def get_customer_details(self, pk):
        customer = Customer.objects.get_by_id(pk)
        customer = CustomerSerializer(customer)
        return response.get_success_200('Customer details loaded successfully', customer.data)
