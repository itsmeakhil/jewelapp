from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from user.service import UserLoginService
from utils import responses as response, logger
from utils.utils import get_client_ip
from user import service as user_service


@permission_classes((AllowAny,))
class UserLogin(APIView):
    service = UserLoginService()

    # # API Documentation for User login API
    # @swagger_auto_schema(
    #     operation_id='',
    #     request_body=openapi.Schema(
    #         type=openapi.TYPE_OBJECT,
    #         properties={
    #             'username': openapi.Schema(
    #                 type=openapi.TYPE_STRING
    #             ),
    #             'password':openapi.Schema(type=openapi.TYPE_STRING)
    #         }
    #     ),
    # )
    def post(self, request):
        """User Login function"""
        try:
            username = request.data.get('username')
            print('user',username)
            password = request.data.get('password')
            return self.service.user_login(username, password)
        except Exception as e:
            logger.error(f'Request -- Error : Login in to system {e}')
            return response.exception_500(e)


class UserLogout(APIView):
    """Logout API View"""
    user_service = user_service.UserLoginService()

    def get(self, request):
        """Function to logout the current user"""
        try:
            ip = get_client_ip(request)
            return self.user_service.logout(request, ip=ip)
        except Exception as e:
            logger.error(
                f'Request by user : {request.user} -- Error : Logging out of the system {e}')
            return response.exception_500(e)
