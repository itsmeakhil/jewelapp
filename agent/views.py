from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from agent import service
from utils import responses as response, logger


class GetAgent(APIView):
    service = service.AgentService()

    def get(self, request):
        """User Login function"""
        try:
            return self.service.get_agent(request)
        except Exception as e:
            logger.error(f'Request -- Error : Login in to system {e}')
            return response.exception_500(e)


class GetContactStatus(APIView):
    service = service.AgentService()

    def get(self, request):
        """User Login function"""
        try:
            return self.service.get_contact_status()
        except Exception as e:
            logger.error(f'Request -- Error : Login in to system {e}')
            return response.exception_500(e)


class GetPhoneNumberStatus(APIView):
    service = service.AgentService()

    def get(self, request):
        """User Login function"""
        try:
            return self.service.get_phone_status()
        except Exception as e:
            logger.error(f'Request -- Error : Login in to system {e}')
            return response.exception_500(e)


class UpdateAgentStatus(APIView):
    service = service.AgentService()

    def post(self, request):
        try:
            return self.service.update_service_Status(data=request.data, user=request.user)
        except Exception as e:
            logger.error(f'Request -- Error : updating customer status in to system {e}')
            return response.exception_500(e)


class UpdatePhoneNumberStatus(APIView):
    service = service.AgentService()

    def post(self, request):
        try:
            return self.service.update_phone_status(data=request.data, user=request.user)
        except Exception as e:
            logger.error(f'Request -- Error : updating phone number status in to system {e}')
            return response.exception_500(e)


class AddQuestionAnswer(APIView):
    service = service.AgentService()

    def post(self, request):
        try:
            return self.service.add_answer(data=request.data)
        except Exception as e:
            logger.error(f'Request -- Error : Question answer in to system {e}')
            return response.exception_500(e)


@permission_classes((AllowAny,))
class AddBulkAgents(APIView):
    service = service.AgentService()

    def post(self, request):
        try:
            return self.service.add_agents(request)
        except Exception as e:
            logger.error(f'Request -- Error : Question answer in to system {e}')
            return response.exception_500(e)


class AddAgentsRemarks(APIView):
    service = service.AgentService()

    def post(self, request):
        try:
            return self.service.add_agent_remarks(data=request.data)
        except Exception as e:
            logger.error(f'Request -- Error : Adding Agents remarks in to system {e}')
            return response.exception_500(e)
