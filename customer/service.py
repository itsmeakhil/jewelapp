import pandas

from customer.models import Customer, CustomerStatusData, ContactStatus
from customer.serializers import CustomerSerializer, ContactStatusSerializer
from questions.models import CustomerAnswers, Question, QuestionOption
from utils import responses as response, logger


class CustomerServicetype:

    def get_customer(self, request):
        if Customer.objects.filter(is_attended=False).exists():
            customer = Customer.objects.get_by_filter(is_attended=False)[0]
            customer.is_attended = True
            customer.save()
            serializer = CustomerSerializer(customer)
            logger.info('Get customer success')
            return response.get_success_200('Customer details loaded successfully', serializer.data)
        logger.error(' No Customer data found ')
        return response.get_success_message('No data found')

    def update_service_Status(self, data, user):
        customer_service_exists = CustomerStatusData.objects.filter(customer=data['customer']).exists()
        status = ContactStatus.objects.get_by_id(data['status'])
        if customer_service_exists:
            customer_service = CustomerStatusData.objects.get(customer=data['customer'])
            status = ContactStatus.objects.get_by_id(data['status'])
            customer_service.status = status
            customer_service.save()
            return response.put_success_message('Updated Customer Service Status')
        customer = Customer.objects.get_by_id(data['customer'])
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
        option = QuestionOption.objects.get_by_id(data['option'])
        if CustomerAnswers.objects.filter(customer=data['customer'], question=data['question']).exists():
            answer = CustomerAnswers.objects.get(customer=data['customer'], question=data['question'])
            answer.option = option.id
            answer.save()
            return response.put_success_message('Answer updated successfully')
        CustomerAnswers.objects.create(customer=customer, question=question, option=option)
        return response.get_success_message('Answer added successfully')

    def add_customers(self, request):
        file = request.FILES['file']
        if file:
            excel_data_df = pandas.read_excel(file, sheet_name='Sheet1')
            data = excel_data_df.to_dict(orient='record')
            for i in data:
                if i['phone_number']:
                    print(i['phone_number'])
                    if i['mobile_number'] == 'nan':
                        i['mobile_number'] = ' '
                    if i['phone_res'] == 'nan':
                        i['phone_res'] = ' '
                    phone_number_exists = Customer.objects.filter(phone_number=i['phone_number']).exists()
                    if not phone_number_exists:
                        cus = Customer.objects.create(name=i['name'], code=i['code'],
                                                      mobile_number=i['mobile_number'],
                                                      phone_number=i['phone_number'], phone_res=i['phone_res'])
                        logger.info(f'Customer Details added : {cus.name}', )
                        print('Added value : ', cus.name)

            return response.post_success('Data added successfully')
