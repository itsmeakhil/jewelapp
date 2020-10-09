from rest_framework import status
from rest_framework.response import Response


def get_success_200(message, data):
    return Response({'message': message, 'status': 200, 'data': data},
                    status=status.HTTP_200_OK)


def get_success_message(message):
    return Response({'message': message, 'status': 200},
                    status=status.HTTP_200_OK)


def set_response(message, code):
    return Response({'message': message, 'status': code},
                    status=status.HTTP_200_OK)


# def get_success_raw_data(message, data):
#     return Response({'message': message, 'status': 200, 'data': data},
#                     status=status.HTTP_200_OK)
#
#
# def post_success_raw_data(message, data):
#     return Response({'message': message, 'status': 200, 'data': data},
#                     status=status.HTTP_200_OK)
#
#
# def post_success_role_permission_data(message, role, permission):
#     return Response({'message': message, 'status': 200, 'roles': role, 'permissions': permission},
#                     status=status.HTTP_200_OK)
#
#
# def get_success_data(serializer):
#     return Response(status=status.HTTP_200_OK, data=serializer)
#
#
# def put_200():
#     return Response({'message': 'Data updated successfully', 'status': 200}, status=status.HTTP_200_OK)
#
#
# def post_created_201(serializer):
#     return Response({'message': 'Data added successfully', 'status': 201, 'data': serializer.data},
#                     status=status.HTTP_201_CREATED)
#
#
# def post_created_201_message(message, serializer):
#     return Response({'message': message, 'status': 201, 'data': serializer.data},
#                     status=status.HTTP_201_CREATED)
#

def delete_success_200(ids_list):
    return Response({'message': f'selected items {ids_list} have been deleted', 'status': 200},
                    status=status.HTTP_200_OK)


def put_success_message(message):
    return Response({'message': message, 'status': 200},
                    status=status.HTTP_200_OK)


def put_success_200(message, data):
    return Response({'message': message, 'status': 200, 'data': data},
                    status=status.HTTP_200_OK)


def serializer_error_400(serializer):
    return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


#
# def already_exist_409():
#     return Response({'message': 'The same item with name already exists'}, status=status.HTTP_409_CONFLICT)
#
#
# def already_exist_message_409(message):
#     return Response({'message': message, 'status': 409}, status=status.HTTP_409_CONFLICT)
#

def no_content_204():
    return Response({'message': 'Nothing selected, Please select data'}, status=status.HTTP_204_NO_CONTENT)


def post_success_201(success_message, data):
    return Response({'message': success_message, 'data': data, 'status': 201}, status=status.HTTP_201_CREATED)


def post_success(success_message):
    return Response({'message': success_message, 'status': 201}, status=status.HTTP_201_CREATED)


def error_response_404(error_message):
    return Response({'message': error_message, 'status': 404}, status=status.HTTP_404_NOT_FOUND)


def error_response_400(error_message):
    return Response({'message': error_message, 'status': 400}, status=status.HTTP_400_BAD_REQUEST)


def exception_500(error):
    return Response({'status': 500, 'message': error.__str__()},
                    status.HTTP_500_INTERNAL_SERVER_ERROR)
