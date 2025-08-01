from rest_framework.exceptions import APIException


class UserNotFoundException(APIException):
    status_code = 404
    default_detail = 'Usuário não encontrado.'
    default_code = 'user_not_found'


class ChatNotFoundException(APIException):
    status_code = 404
    default_detail = 'Chat não encontrado e/ou não pertenece ao usuário.'
    default_code = 'chat_not_found'