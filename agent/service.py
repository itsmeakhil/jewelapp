import math

import pandas

from agent.models import AgentStatus, ContactStatus, Agent, AgentPhoneNumber, PhoneNumberStatus
from agent.serializers import AgentSerializer, ContactStatusSerializer, PhoneNumberStatusSerializer
from questions.models import AgentAnswers, Question, QuestionOption
from utils import responses as response, logger, constants


class AgentService:
    def get_agent(self, request):
        if Agent.objects.filter(is_attended=False).exists():
            agent = Agent.objects.get_by_filter(is_attended=False)[0]
            serializer = AgentSerializer(agent)
            logger.info('Get agent success')
            return response.get_success_200('Customer details loaded successfully', serializer.data)
        logger.error(' No Customer data found ')
        return response.get_success_message('No data found')

    def update_service_Status(self, data, user):
        agent_status_exists = AgentStatus.objects.filter(agent=data['agent']).exists()
        status = ContactStatus.objects.get_by_id(data['status'])
        agent = Agent.objects.get_by_id(data['agent'])
        if agent_status_exists:
            agent_status = AgentStatus.objects.get(agent=data['agent'])
            status = ContactStatus.objects.get_by_id(data['status'])
            agent_status.status = status
            agent_status.user = user
            agent_status.save()
            agent.is_attended = True
            agent.save()
            return response.put_success_message('Updated Customer Service Status')
        AgentStatus.objects.create(agent=agent, user=user, status=status)
        return response.post_success('Added Customer Status Data')

    def get_contact_status(self):
        contact_status = ContactStatus.objects.get_all_active()
        serializer = ContactStatusSerializer(contact_status, many=True)
        logger.info('GET Contact status success')
        return response.get_success_200('Contact status loaded successfully', serializer.data)

    def get_phone_status(self):
        phone_number_status = PhoneNumberStatus.objects.get_all_active()
        serializer = PhoneNumberStatusSerializer(phone_number_status, many=True)
        logger.info('Phone status list loaded successfully')
        return response.get_success_200('Phone status loaded successfully', serializer.data)

    def update_phone_status(self, data, user):
        phone_exists = AgentPhoneNumber.objects.filter(phone_number=data['phone_number']).exists()
        if phone_exists:
            status = PhoneNumberStatus.objects.get(data['status'])
            phone = AgentPhoneNumber.objects.get(phone_number=data['phone_number'])
            phone.status = status
            phone.save()
            return response.put_success_message('Updated Agent Phone Number')
        return response.error_response_400('Unable to find the Phone number ')

    def add_answer(self, data):
        agent = Agent.objects.get_by_id(data['agent'])
        question = Question.objects.get_by_id(data['question'])
        if not data['option']:
            AgentAnswers.objects.get(agent=data['agent'], question=data['question']).delete()
            return response.get_success_message('Response deleted')
        if AgentAnswers.objects.filter(agent=data['agent'], question=data['question']).exists():
            option = QuestionOption.objects.get_by_id(data['option'])
            answer = AgentAnswers.objects.get(agent=data['agent'], question=data['question'])
            answer.option = option
            answer.save()
            return response.put_success_message('Answer updated successfully')
        option = QuestionOption.objects.get_by_id(data['option'])
        AgentAnswers.objects.create(agent=agent, question=question, option=option)
        return response.get_success_message('Answer added successfully')

    def add_agents(self, request):
        file = request.FILES['file']
        if file:
            excel_data_df = pandas.read_excel(file, sheet_name='Sheet1')
            data = excel_data_df.to_dict(orient='record')
            for i in data:
                serializer = AgentSerializer(data=i)
                if serializer.is_valid():
                    agent = serializer.save()
                if not math.isnan(i['phone_number1']):
                    if not AgentPhoneNumber.objects.get_by_filter(phone_number=int(i['phone_number1'])).exists():
                        status = PhoneNumberStatus.objects.get(name=constants.ACTIVE)
                        AgentPhoneNumber.objects.create(agent=agent, phone_number=i['phone_number1'], status=status)
                if not math.isnan(i['phone_number2']):
                    if not AgentPhoneNumber.objects.get_by_filter(phone_number=int(i['phone_number2'])).exists():
                        status = PhoneNumberStatus.objects.get(name=constants.ACTIVE)
                        AgentPhoneNumber.objects.create(agent=agent, phone_number=i['phone_number2'], status=status)
                if not math.isnan(i['phone_number3']):
                    if not AgentPhoneNumber.objects.get_by_filter(phone_number=int(i['phone_number3'])).exists():
                        status = PhoneNumberStatus.objects.get(name=constants.ACTIVE)
                        AgentPhoneNumber.objects.create(agent=agent, phone_number=i['phone_number3'], status=status)
            return response.post_success('Data added successfully')