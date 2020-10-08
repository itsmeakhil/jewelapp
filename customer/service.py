from questions.models import CustomerAnswers, Question, QuestionOption
from utils import responses as response, constants, logger
from customer.models import Customer, CustomerStatusData, ContactStatus
from customer.serializers import CustomerSerializer, ContactStatusSerializer


class CustomerServicetype:

    def get_customer(self, request):
        if Customer.objects.filter(is_attended=False).exists():
            customer = Customer.objects.get_by_filter(is_attended=False)[0]
            customer.is_attended = True
            customer.save()
            status = ContactStatus.objects.get(name="Attended")
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
            return response.post_success('Updated Customer Service Status')
        customer = Customer.objects.get_by_id(data['customer'])
        CustomerStatusData.objects.create(customer=customer, user=user, status=status)
        return response.post_success('Added Customer Status Data')

    def get_contact_status(self, company):
        contact_status = ContactStatus.objects.filter(company=company)
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
