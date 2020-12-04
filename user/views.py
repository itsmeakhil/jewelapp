from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from user.service import UserLoginService
from utils import responses as response, logger
from utils.utils import get_client_ip
from user import service as user_service

service = UserLoginService()


@permission_classes((AllowAny,))
class UserLogin(APIView):

    def post(self, request):
        """User Login function"""
        try:
            username = request.data.get('username')
            print('user',username)
            password = request.data.get('password')
            return service.user_login(username, password)
        except Exception as e:
            logger.error(f'Request -- Error : Login in to system {e}')
            return response.exception_500(e)


@permission_classes((AllowAny,))
class UserLoginV1(APIView):


    def post(self, request):
        """User Login function"""
        try:
            username = request.data.get('username')
            print('user',username)
            password = request.data.get('password')
            return service.user_login_v1(username, password)
        except Exception as e:
            logger.error(f'Request -- Error : Login in to system {e}')
            return response.exception_500(e)


class UserLogout(APIView):
    """Logout API View"""

    def get(self, request):
        """Function to logout the current user"""
        try:
            ip = get_client_ip(request)
            return service.logout(request,ip=ip)
        except Exception as e:
            logger.error(
                f'Request by user : {request.user} -- Error : Logging out of the system {e}')
            return response.exception_500(e)



class GetFieldAgent(APIView):

    def get(self, request):
        """Function to logout the current user"""
        try:
            return service.get_field_agent()
        except Exception as e:
            logger.error(
                f'Request by user : {request.user} -- Error : Logging out of the system {e}')
            return response.exception_500(e)


