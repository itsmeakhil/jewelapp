import errno
import os
from datetime import datetime
from random import randint

from django.db import transaction

from utils import logger
from user.models import User

def delete_instance(instance):
    """
    to change the status of an instance instead of delete
    :param instance: object
    :return: success message
    """
    # Updates the is deleted and is active values
    logger.debug(f'Updating the is active and is deleted value of the {instance}')
    instance.is_active = False

    instance.is_deleted = True
    with transaction.atomic():
        # Saves the  updated instance to the database
        instance.save()
        logger.debug(f'Updated the is active and is deleted value of instance {instance} successfully')
#
#
# def generate_key():
#     """ User otp key generator """
#     key = pyotp.random_base32()
#     if is_unique(key):
#         return key


def is_unique(key):
    try:
        # checking whether the generated key already exists or not
        User.objects.get(key=key)
    except User.DoesNotExist:
        return True
    return False


def visitors_otp(n):
    """Visitor otp generator"""
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def get_unique_id(n):
    """
    Function to generate the unique id of the complaints
    """
    date_code = datetime.now()
    const = 1000
    date_code = date_code.strftime("%d%m")

    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    code = randint(range_start, range_end)

    return f'CMP{date_code}{code}'


def get_date():
    date = datetime.now()
    return date


# Method to get client ip
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def log_file_exists(filepath):
    if not os.path.exists(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath))
            return True
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                return False
