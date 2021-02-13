from datetime import datetime

import pandas
from django.db import transaction
from django.db.models import Q

from agent.models import ContactStatus, PhoneNumberStatus
from customer.models import CustomerPhoneNumber, CustomerRemarks, CustomerFieldReport, Customer, CustomerStatus, \
    CustomerFieldAgent, CustomerWithFieldReport
from customer.serializers import CustomerRemarksSerializer, CustomerSerializer, CustomerGetSerializer, \
    CustomerFieldAgentGetReportSerializer, CustomerFieldReportGetSerializer, CustomerFieldReportSerializer, \
    CustomerFieldAgentReportSerializer, CustomerPhoneNumberSerializer, CustomerWithFieldReportGetSerializer
from user.models import User
from utils import responses as response, logger, constants


class CustomerService:
    def get_customer(self):
        with transaction.atomic():
            if Customer.objects.filter(is_attended=False).exists():
                customer = Customer.objects.get_by_filter(is_attended=False)[0]
                if CustomerFieldReport.objects.get_by_filter(customer=customer.id).exists():
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
                customer.is_attended = True
                customer.save()
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
            print(phone_exists)
            status = PhoneNumberStatus.objects.get_by_id(data['status'])
            print(status)
            phone = CustomerPhoneNumber.objects.get_by_filter(phone_number=data['phone_number']).first()
            print(phone)
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

    def add_customer_remarks(self, data, user):
        with transaction.atomic():
            serializer = CustomerRemarksSerializer(data=data)
            if serializer.is_valid():
                serializer.save(user=user)
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
                        serializer.save()
                        customer = Customer.objects.get_by_id(i)
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
                            cus_field_agent_data.status = 2
                            serialized_data.save()
                            cus_field_agent_data.save()
                            if CustomerWithFieldReport.objects.get_by_filter(customer=data['customer']).exists():
                                customer_with_report = \
                                    CustomerWithFieldReport.objects.get_by_filter(customer=data['customer'])[0]
                                customer_with_report.last_call_date = datetime.now()
                                customer_with_report.save()
                            user = User.objects.get_by_id(pk=1)
                            customer = Customer.objects.get_by_id(data['customer'])
                            CustomerWithFieldReport.objects.create(customer=customer, user=user)
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
                        if data['phone_number']:
                            status = PhoneNumberStatus.objects.get(name=constants.ACTIVE)
                            for i in data['phone_number']:
                                if not CustomerPhoneNumber.objects.get_by_filter(phone_number=int(i)).exists():
                                    customer = Customer.objects.get_by_id(field_data.customer.id)
                                    CustomerPhoneNumber.objects.create(customer=customer,
                                                                       phone_number=int(i),
                                                                       status=status)
                        serialized_data.save()
                        return response.post_success_201('Field Report added successfully', serialized_data.data)
                    return response.serializer_error_400(serialized_data)
                return response.error_response_400('Field report for the customer not found ')
            return response.error_response_400('Invalid data format ')

    def get_customer_details(self, pk):
        customer = Customer.objects.get_by_id(pk)
        customer = CustomerSerializer(customer)
        return response.get_success_200('Customer details loaded successfully', customer.data)

    def update_customer(self, data, pk):
        with transaction.atomic():
            if data:
                if Customer.objects.get_by_id(pk):
                    customer_data = Customer.objects.get_by_id(pk)
                    serialized_data = CustomerSerializer(customer_data, data=data)
                    if serialized_data.is_valid():
                        serialized_data.save()
                        return response.put_success_200('Customer details updated successfully', serialized_data.data)
                    return response.serializer_error_400(serialized_data)
                return response.error_response_404('Customer not found ')
            return response.error_response_400('Invalid data format ')

    def update_phone_number(self, data, pk):
        phone_exists = CustomerPhoneNumber.objects.get_by_filter(id=pk).exists()
        if phone_exists:
            phone_number = CustomerPhoneNumber.objects.get_by_id(pk)
            serializer = CustomerPhoneNumberSerializer(phone_number, data=data)
            if serializer.is_valid():
                serializer.save()
                return response.put_success_message('Updated Customer Phone Number')
            return response.error_response_400(f'Data is invalid ')
        return response.error_response_400('Unable to find the Phone number ')

    def get_all_customers_with_filed_report(self, query, user):
        query_set = (Q(user=user) | Q(user=1))
        customer = CustomerWithFieldReport.objects.get_all()
        customer = customer.filter(query_set)
        if query:
            customer = customer.filter(customer__bride_name__icontains=query)
        # customer = customer.order_by('-last_call_date')
        serializer = CustomerWithFieldReportGetSerializer(customer, many=True)
        return response.get_success_200('Customer list loaded successfully', serializer.data)

    def get_customer_details_with_field_report(self, pk, user):
        if Customer.objects.get_by_filter(id=pk):
            customer = Customer.objects.get_by_id(pk)
            if CustomerFieldReport.objects.get_by_filter(customer=pk).exists():
                if CustomerWithFieldReport.objects.get_by_filter(customer=pk)[0]:
                    data = CustomerWithFieldReport.objects.get_by_filter(customer=pk)[0]
                    if data.user.id == 1 or data.user.id == user.id:
                        pass
                    else:
                        return response.error_response_400('User already assigned and called customer')
                    data.user = user
                    data.save()
                field_report = CustomerFieldReport.objects.get_by_filter(customer=pk)[0]
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
            customer.is_attended = True
            customer.save()
        logger.error(' No Customer data found ')
        return response.get_success_message('No data found')

    def add_bulk_customers(self, request):
        file = request.FILES['file']
        print(file)
        if file:
            excel_data_df = pandas.read_excel(file, sheet_name='Sheet1')
            data = excel_data_df.to_dict(orient='record')
            status = PhoneNumberStatus.objects.get(name=constants.ACTIVE)
            x = 1
            print(data)
            for i in data:
                m = "hcsahh"
                f = 100.00
                m_type = type(m)  # Do not remove this
                f_type = type(f)
                n_type = type(i['bride_name'])
                father_type = type(i['name_of_father'])
                mother_type = type(i['name_of_mother'])
                if n_type == m_type or father_type == m_type or mother_type == m_type:

                    if type(i['house_name']) == f_type:
                        i.update({'house_name': ""})
                    if type(i['bride_name']) == f_type:
                        i.update({'bride_name': ""})
                    if type(i['name_of_father']) == f_type:
                        i.update({'name_of_father': ""})
                    if type(i['name_of_mother']) == f_type:
                        i.update({'name_of_mother': ""})
                    if type(i['month']) == f_type:
                        i.update({'month': ""})
                    if type(i['place']) == f_type:
                        i.update({'place': ""})
                    if type(i['phone_number1']) == f_type:
                        i.update({'phone_number1': ""})
                    if type(i['phone_number2']) == f_type:
                        i.update({'phone_number2': ""})
                    if type(i['phone_number3']) == f_type:
                        i.update({'phone_number3': ""})

                    ph1_exists = True
                    ph2_exists = True
                    ph3_exists = True

                    if i['phone_number1']:
                        ph1_exists = CustomerPhoneNumber.objects.get_by_filter(
                            phone_number=int(i['phone_number1'])).exists()
                    if i['phone_number2']:
                        ph2_exists = CustomerPhoneNumber.objects.get_by_filter(
                            phone_number=int(i['phone_number2'])).exists()
                    if i['phone_number3']:
                        ph3_exists = CustomerPhoneNumber.objects.get_by_filter(
                            phone_number=int(i['phone_number3'])).exists()
                    print('----------------------', x)
                    x +=1
                    print(ph1_exists, ph2_exists, ph3_exists)
                    if not ph1_exists or not ph2_exists or not ph3_exists:
                        serializer = CustomerSerializer(data=i)
                        if serializer.is_valid():
                            customer = serializer.save()
                            print(i)
                            if not ph1_exists:
                                CustomerPhoneNumber.objects.create(customer=customer,
                                                                   phone_number=int(i['phone_number1']),
                                                                   status=status)
                            if not ph2_exists:
                                CustomerPhoneNumber.objects.create(customer=customer,
                                                                   phone_number=int(i['phone_number2']),
                                                                   status=status)
                            if not ph3_exists:
                                CustomerPhoneNumber.objects.create(customer=customer,
                                                                   phone_number=int(i['phone_number3']),
                                                                   status=status)
        return response.post_success('Data added successfully')
