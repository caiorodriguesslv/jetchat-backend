from accounts.models import User
from django.contrib.auth.hashers import check_password, make_password


class Authentication:
    """Classe responsável pela autenticação de usuários."""

    def signIn(self, email: str, password: str) -> User | bool:
        """
        Autentica um usuário com base no e-mail e senha fornecidos.
        """
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                return user
            return False
            
        except User.DoesNotExist:
            return False

        except Exception as e:
            print(f"Erro ao autenticar usuário: {e}")
            return False

    def signUp(self, email: str, password: str, name: str) -> User:
        """
        Registra um novo usuário com o e-mail, senha e nome fornecidos.
        """
        if User.objects.filter(email=email).exists():
            raise ValueError("Usuário já existe com este e-mail.")

        try:
            user = User.objects.create(
                email=email,
                password=make_password(password),
                name=name
            )
            return user

        except Exception as e:
            print(f"Erro ao registrar usuário: {e}")
            return None