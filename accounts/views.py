from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed

from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils.timezone import now

from rest_framework_simplejwt.tokens import RefreshToken

from accounts.auth import Authentication
from accounts.serializers import UserSerializer
from accounts.models import User

from core.utils.exceptions import ValidationError


class SignInView(APIView, Authentication):
    permission_classes = [AllowAny] # Permite acesso a qualquer usuário, autenticado ou não

    def post(self, request):
        """       
         Realiza o login do usuário com base no e-mail e senha fornecidos.
        """
        email = request.data.get('email', '')
        password = request.data.get('password', '') 

        signin =  self.signIn(email, password)

        if not signin:
            raise AuthenticationFailed('E-mail ou senha inválidos.')

        user = UserSerializer(signin).data # Serializa os dados do usuário autenticado
        access_token = RefreshToken.for_user(signin).access_token # Gera o token de acesso

        
        return Response({
            'user': user,
            'access_token': str(access_token),
            'refresh_token': str(RefreshToken.for_user(signin))
        }, status=200)