from datetime import date, datetime

import pandas
from django.db import transaction

from agent.models import AgentStatus, ContactStatus, Agent, AgentPhoneNumber, PhoneNumberStatus, Recall
from agent.serializers import AgentSerializer, ContactStatusSerializer, PhoneNumberStatusSerializer, \
    AgentRemarksSerializer, RecallSerializer
from questions.models import AgentAnswers, Question, QuestionOption
from utils import responses as response, logger, constants


class AgentService:
    def get_agent(self, request):
        if Recall.objects.get_by_filter(status=1, date=date.today(), time__gte=datetime.now().time()):
            recall = Recall.objects.get_by_filter(status=1, date=date.today(), time__lte=datetime.now().time())
            recall.status = 2
            recall.save()
            agent = Agent.objects.get_by_id(recall.agent.id)
            serializer = AgentSerializer(agent)
            agent.is_assigned = True
            agent.save()
            return response.get_success_200('Agent details loaded successfully', serializer.data)

        elif Agent.objects.filter(is_assigned=False).exists():
            agent = Agent.objects.get_by_filter(is_assigned=False)[0]
            serializer = AgentSerializer(agent)
            agent.is_assigned = True
            agent.save()
            logger.info('Get agent success')
            return response.get_success_200('Agent details loaded successfully', serializer.data)
        else:
            logger.error(' No Agent data found ')
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
        print(data)
        phone_exists = AgentPhoneNumber.objects.filter(phone_number=data['phone_number']).exists()
        print(phone_exists)
        if phone_exists:
            status = PhoneNumberStatus.objects.get_by_id(data['status'])
            print(status)
            phone = AgentPhoneNumber.objects.get(phone_number=data['phone_number'])
            print(phone)
            phone.status = status
            phone.save()
            return response.put_success_message('Updated Agent Phone Number')
        return response.error_response_400('Unable to find the Phone number ')

    def add_answer(self, data):
        with transaction.atomic():
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
                return response.put_success_200('Answer updated successfully', data={})
            option = QuestionOption.objects.get_by_id(data['option'])
            AgentAnswers.objects.create(agent=agent, question=question, option=option)
            return response.get_success_200('Answer added successfully', data={})

    def add_agents(self, request):
        file = request.FILES['file']
        if file:
            excel_data_df = pandas.read_excel(file, sheet_name='Sheet1')
            data = excel_data_df.to_dict(orient='record')
            status = PhoneNumberStatus.objects.get(name=constants.ACTIVE)
            x = 1
            for i in data:
                m = "hcsahh"
                f = 100.00
                m_type = type(m)  # Do not remove this
                f_type = type(f)
                n_type = type(i['name'])
                sec_type = type(i['second_name'])
                if n_type == m_type or sec_type == m_type:
                    if n_type == f_type:
                        i.update({'name': i['second_name']})
                    if type(i['address']) == f_type:
                        i.update({'address': ""})
                    if type(i['code']) == f_type:
                        i.update({'code': ""})
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
                        ph1_exists = AgentPhoneNumber.objects.get_by_filter(
                            phone_number=int(i['phone_number1'])).exists()
                    if i['phone_number2']:
                        ph2_exists = AgentPhoneNumber.objects.get_by_filter(
                            phone_number=int(i['phone_number2'])).exists()
                    if i['phone_number3']:
                        ph3_exists = AgentPhoneNumber.objects.get_by_filter(
                            phone_number=int(i['phone_number3'])).exists()

                    if not ph1_exists or not ph2_exists or not ph3_exists:
                        serializer = AgentSerializer(data=i)
                        if serializer.is_valid():
                            agent = serializer.save()

                            if not ph1_exists:
                                AgentPhoneNumber.objects.create(agent=agent, phone_number=int(i['phone_number1']),
                                                                status=status)
                            if not ph2_exists:
                                AgentPhoneNumber.objects.create(agent=agent, phone_number=int(i['phone_number2']),
                                                                status=status)
                            if not ph3_exists:
                                AgentPhoneNumber.objects.create(agent=agent, phone_number=int(i['phone_number3']),
                                                                status=status)
        return response.post_success('Data added successfully')

    def add_agent_remarks(self, data):
        with transaction.atomic():
            serializer = AgentRemarksSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return response.post_success_201('Successfully added Remarks ', serializer.data)
            return response.serializer_error_400(serializer)

    def add_question_remarks(self, data):
        with transaction.atomic():
            if AgentAnswers.objects.filter(agent=data['agent'], question=data['question']).exists():
                answer = AgentAnswers.objects.get(agent=data['agent'], question=data['question'])
                answer.remarks = data['remarks']
                answer.save()
                return response.put_success_message('Answer remarks added successfully')
            return response.error_response_400('Answer not found.')

    def add_recall(self, data):
        with transaction.atomic():
            if not Recall.objects.filter(agent=data['agent']).exists():
                serializer = RecallSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return response.put_success_message('Recall added successfully')
                return response.error_response_400('Data is incorrect')
            recall = Recall.objects.get_by_filter(agent=data['agent'])[0]
            serializer = RecallSerializer(recall, data=data)
            if serializer.is_valid():
                serializer.save()
                return response.put_success_message('Recall added successfully')
            return response.error_response_400('Data is incorrect')
