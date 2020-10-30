import math

import pandas

from customer.models import CustomerStatusData, ContactStatus, Customer
from customer.serializers import CustomerSerializer, ContactStatusSerializer
from questions.models import CustomerAnswers, Question, QuestionOption
from utils import responses as response, logger


class CustomerServicetype:

    def get_customer(self, request):
        if Customer.objects.filter(is_attended=False).exists():
            customer = Customer.objects.get_by_filter(is_attended=False)[0]
            serializer = CustomerSerializer(customer)
            logger.info('Get customer success')
            return response.get_success_200('Customer details loaded successfully', serializer.data)
        logger.error(' No Customer data found ')
        return response.get_success_message('No data found')

    def update_service_Status(self, data, user):
        customer_service_exists = CustomerStatusData.objects.filter(customer=data['customer']).exists()
        status = ContactStatus.objects.get_by_id(data['status'])
        customer = Customer.objects.get_by_id(data['customer'])
        if customer_service_exists:
            customer_service = CustomerStatusData.objects.get(customer=data['customer'])
            status = ContactStatus.objects.get_by_id(data['status'])
            customer_service.status = status
            customer_service.user = user
            customer_service.save()
            customer.is_attended = True
            customer.save()
            return response.put_success_message('Updated Customer Service Status')
        CustomerStatusData.objects.create(customer=customer, user=user, status=status)
        return response.post_success('Added Customer Status Data')

    def get_contact_status(self):
        contact_status = ContactStatus.objects.get_all_active()
        serializer = ContactStatusSerializer(contact_status, many=True)
        logger.info('GET Contact status success')
        return response.get_success_200('Contact status loaded successfully', serializer.data)

    def add_question_response(self, data):
        for i in data:
            customer = Customer.objects.get_by_id(i['customer'])
            question = Question.objects.get_by_id(i['question'])
            option = QuestionOption.objects.get_by_id(i['option'])
            CustomerAnswers.objects.create(customer=customer, question=question, option=option)
        return response.post_success('Answers added successfully')

    def add_answer(self, data):
        customer = Customer.objects.get_by_id(data['customer'])
        question = Question.objects.get_by_id(data['question'])
        if not data['option']:
            CustomerAnswers.objects.get(customer=data['customer'], question=data['question']).delete()
            return response.get_success_message('Response deleted')
        if CustomerAnswers.objects.filter(customer=data['customer'], question=data['question']).exists():
            option = QuestionOption.objects.get_by_id(data['option'])
            answer = CustomerAnswers.objects.get(customer=data['customer'], question=data['question'])
            answer.option = option
            answer.save()
            return response.put_success_message('Answer updated successfully')
        option = QuestionOption.objects.get_by_id(data['option'])
        CustomerAnswers.objects.create(customer=customer, question=question, option=option)
        return response.get_success_message('Answer added successfully')

    def add_customers(self, request):
        file = request.FILES['file']
        if file:
            excel_data_df = pandas.read_excel(file, sheet_name='Sheet1')
            data = excel_data_df.to_dict(orient='record')
            for i in data:
                if i['phone_number']:
                    print('1')
                    if i['mobile_number']:
                        print('11')
                        if not math.isnan(i['mobile_number']):
                            i['mobile_number'] = int(i['mobile_number'])
                        else:
                            i['mobile_number'] = ' '
                    if i['phone_res']:
                        print('111')
                        if not math.isnan(i['phone_res']):
                            i['phone_res'] = int(i['phone_res'])
                        else:
                            i['phone_res'] = ' '
                    phone_number_exists = Customer.objects.filter(phone_number=i['phone_number']).exists()

                    if not phone_number_exists:
                        # i['group'] = int(i['group'])
                        print('1111')
                        serializer = CustomerSerializer(data=i)
                        if serializer.is_valid():
                            print('11111')
                            serializer.save()
                            logger.info(f'Customer Details added : {serializer.data}', )
                            print('Added value : ', serializer.data)
                        print(serializer.errors)

            return response.post_success('Data added successfully')
