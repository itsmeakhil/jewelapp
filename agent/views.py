from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from agent import service
from utils import responses as response, logger

service = service.AgentService()


class GetAgent(APIView):

    def get(self, request):
        try:
            return service.get_agent(request)
        except Exception as e:
            logger.error(f'Request -- Error : Getting agent details from system {e}')
            return response.exception_500(e)


class GetContactStatus(APIView):

    def get(self, request):
        try:
            return service.get_contact_status()
        except Exception as e:
            logger.error(f'Request -- Error : Getting contact status from system {e}')
            return response.exception_500(e)


class GetPhoneNumberStatus(APIView):

    def get(self, request):
        try:
            return service.get_phone_status()
        except Exception as e:
            logger.error(f'Request -- Error : Getting phone number status from system {e}')
            return response.exception_500(e)


class UpdateAgentStatus(APIView):

    def post(self, request):
        try:
            return service.update_service_Status(data=request.data, user=request.user)
        except Exception as e:
            logger.error(f'Request -- Error : updating agent status in to system {e}')
            return response.exception_500(e)


class UpdatePhoneNumberStatus(APIView):

    def post(self, request):
        try:
            return service.update_phone_status(data=request.data, user=request.user)
        except Exception as e:
            logger.error(f'Request -- Error : updating phone number status in to system {e}')
            return response.exception_500(e)


class AddQuestionAnswer(APIView):

    def post(self, request):
        try:
            return service.add_answer(data=request.data)
        except Exception as e:
            logger.error(f'Request -- Error : Question answer in to system {e}')
            return response.exception_500(e)

class AddQuestionRemarks(APIView):

    def post(self, request):
        try:
            return service.add_question_remarks(data=request.data)
        except Exception as e:
            logger.error(f'Request -- Error : Question remarks in to system {e}')
            return response.exception_500(e)


@permission_classes((AllowAny,))
class AddBulkAgents(APIView):

    def post(self, request):
        try:
            return service.add_agents(request)
        except Exception as e:
            logger.error(f'Request -- Error : Question answer in to system {e}')
            return response.exception_500(e)


class AddAgentsRemarks(APIView):

    def post(self, request):
        try:
            return service.add_agent_remarks(data=request.data)
        except Exception as e:
            logger.error(f'Request -- Error : Adding Agents remarks in to system {e}')
            return response.exception_500(e)
