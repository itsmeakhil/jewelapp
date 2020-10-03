from django.contrib.auth import logout, authenticate
from django.db import transaction
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from utils import responses as response, constants, logger
from user.models import User
from rest_framework.authtoken.models import Token
from user import serializers as user_serializer


class UserLoginService:

    def user_login(self, username, password):
        user = User.objects.get(username=username)
        user_auth = authenticate(username=username, password=password)
        print('user auth', user_auth)
        if user_auth:
            # if pbkdf2_sha256.verify(password, user.password):
            token, _ = Token.objects.get_or_create(user=user)
            print(token.key)
            user_data = user_serializer.UserSerializer(user)
            data = {
                "token": token.key,
                "status": 200,
                "user": user_data.data,
            }
            logger.info('User login Success')
            return response.get_success_200('User verification successful', data)
        return response.error_response_404('Email or Password is incorrect, please check the password and try again')
        # logger.error(' The employee id or password you entered is incorrect ')
        # return response.error_response_404('Unable to find the user')

    def logout(self, request, ip):
        """Function to logout the current user"""
        with transaction.atomic():
            logout(request)
            logger.info(f"Request by user: {request.user} -- from ip : {ip} -- logout successfully ")
            return response.get_success_message('User logged out successfully')
