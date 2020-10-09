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
        # user_auth = authenticate(username=username, password=password)
        # print('user auth', user_auth)
        if user:
            if pbkdf2_sha256.verify(password, user.password):
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
            data = {
                "status": 400,
                "message": 'Email or Password is incorrect, please check the password and try again'
            }
            return response.get_success_200(data)
        logger.error(' The employee id or password you entered is incorrect ')
        data = {
            "status": 400,
            "message": 'Unable to find the user'
        }
        return response.get_success_200(data)

    def user_login_v1(self, username, password):
        print('herer')
        user_exists = User.objects.filter(username=username).exists()
        print(user_exists)
        # user_auth = authenticate(username=username, password=password)
        # print('user auth', user_auth)
        if user_exists:
            user = User.objects.get(username=username)
            if user.password == password:
                token, _ = Token.objects.get_or_create(user=user)
                user_data = user_serializer.UserSerializer(user)
                data = {
                    "token": token.key,
                    "user": user_data.data,
                }
                logger.info('User login Success')
                return response.get_success_200('User login successful', data)
            return response.error_response_400(' Password is incorrect, please check the password and try again')
        logger.error(' The employee id or password you entered is incorrect ')
        return response.error_response_400('Unable to find the user, Please check the username and try again')

    def logout(self, request, ip):
        """Function to logout the current user"""
        with transaction.atomic():
            logout(request)
            logger.info(f"Request by user: {request.user} -- from ip : {ip} -- logout successfully ")
            return response.get_success_message('User logged out successfully')
