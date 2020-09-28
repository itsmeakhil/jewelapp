from django.contrib.auth import logout, authenticate
from django.db import transaction

from utils import responses as response, constants, logger
from user.models import User
from rest_framework.authtoken.models import Token
from user import serializers as user_serializer


class UserLoginService:

    def user_login(self, request):
        user_exists = User.objects.filter(username=request.data.get('username')).exists()
        if user_exists:
            user = User.objects.get(username=request.data.get('username'))
            if user.password==request.data.get('password'):
                token, _ = Token.objects.get_or_create(user=user)
                user_data = user_serializer.UserSerializer(user)
                data = {
                    "token": token.key,
                    "status": 200,
                    "user": user_data.data,
                }
                logger.info('User login Success')
                return response.get_success_200('User verification successful', data)
            return response.error_response_404('Password incorrect')
        logger.error(' The employee id not found ')
        return response.error_response_404('Email or password is incorrect, please check the password and try again')

    def logout(self, request, ip):
        """Function to logout the current user"""
        with transaction.atomic():
            logout(request)
            logger.info(f"Request by user: {request.user} -- from ip : {ip} -- logout successfully ")
            return response.get_success_message('User logged out successfully')
