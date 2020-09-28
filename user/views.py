from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from utils import responses as response,logger
from utils.utils import get_client_ip
from user import service as user_service
from user.models import User




@permission_classes((AllowAny,))
class UserLogin(APIView):
    user_service = user_service.UserLoginService()

    # API Documentation for User login API
    @swagger_auto_schema(
        operation_id='',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'phone_number': openapi.Schema(
                    type=openapi.TYPE_STRING
                )
            }
        ),
    )
    def post(self, request):
        """User Login function"""
        try:
            return self.user_service.user_login(request)
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
