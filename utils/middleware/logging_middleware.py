from django.contrib.auth.models import AnonymousUser

from utils.utils import logger_obj as access_logs, get_client_ip

login_method_name = 'login'


class APILoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        ip = get_client_ip(request)
        user = request.user if type(
            request.user) is not AnonymousUser else 'Anonymous User'

        log_msg = f'API request {request}, from {ip} by {user}'
        try:
            if request.data is not None and not request.path.__contains__(
                    login_method_name):
                log_msg = log_msg + f'data : {request.data}'
        except Exception as e:
            access_logs.error(e)
        access_logs.info(log_msg)

        # Code to be executed for each request/response after
        # the view is called.

        if response and response[
            'content-type'] == 'application/json' and \
                not request.path.__contains__(login_method_name):
            response_body = response.content
            access_logs.info(
                f'API response {response_body} to {ip} for {request} by {user}')

        return response
