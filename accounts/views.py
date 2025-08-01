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

import uuid

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


class SignUpView(APIView, Authentication):
    permission_classes = [AllowAny] # Permite acesso a qualquer usuário, autenticado ou não

    def post(self, request):
        """
        Realiza o cadastro de um novo usuário com base nos dados fornecidos.
        """
        name = request.data.get('name', '')
        email = request.data.get('email', '')
        password = request.data.get('password', '')
    
        if not name or not email or not password:
            raise AuthenticationFailed('Todos os campos são obrigatórios.')

        signup = self.signUp(email, password, name)

        if not signup:
            raise AuthenticationFailed('Erro ao criar usuário.')

        """
        Nesse caso, o usuário é criado e já autenticado automaticamente.
        Isso significa que, após o cadastro, o usuário receberá um token de acesso imediatamente.

        """
        user = UserSerializer(signup).data 
        access_token = RefreshToken.for_user(signup).access_token

        return Response({
            'user': user,
            'access_token': str(access_token),
            'refresh_token': str(RefreshToken.for_user(signup))
        }, status=201)


class UserView(APIView):
    def get(self, request):
        """
        Retorna os dados do usuário autenticado.
        """

        # Atualiza o campo last_access do usuário com a data e hora atual
        User.objects.filter(email=request.user.email).update(last_access=now())


        user = UserSerializer(request.user).data


        return Response({
            "user": user,
        }, status=200)

    def put(self, request):
        """
        Atualiza os dados do usuário autenticado.
        """
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')
        avatar = request.FILES.get('avatar') 


        # Inicializa o storage 
        storage = FileSystemStorage(
            location=settings.MEDIA_ROOT / 'avatars',
            base_url=settings.MEDIA_URL + 'avatars/'
        )
      
        # Verifica se o usuário está autenticado e validado
        if avatar:
            content_type = avatar.content_type
            extension = avatar.name.split('.')[-1].lower() # Verifica a extensão do arquivo e pega o último item após o ponto
            if content_type not in ['image/jpeg', 'image/png']:
                raise ValidationError('Formato de imagem inválido. Somente JPEG e PNG são permitidos.')

        # Salva o avatar 
        file  = storage.save(f"{uuid.uuid4()}.{extension}", avatar) if avatar else None
        avatar = storage.url(file) if file else None

        serializer = UserSerializer(request.user, data={
            'name': name,
            'email': email,
            'avatar': avatar or request.user.avatar,
        }, partial=True)

        if not serializer.is_valid():
            # Deleta o arquivo se a validação falhar
            if avatar:
                storage.delete(avatar.split('/')[-1])  

            first_error = list(serializer.errors.values())[0][0]


        # Deleta o avatar antigo se um novo for fornecido
        if avatar and request.user.avatar != 'media/avatars/default-avatar.png':
            storage.delete(request.user.avatar.split('/')[-1])  


        # Atualizar o password se fornecido
        if password:
            request.user.set_password(password)
            

        serializer.save()

        return Response({
            'user': serializer.data,
            'message': 'Usuário atualizado com sucesso.'
        }, status=200)