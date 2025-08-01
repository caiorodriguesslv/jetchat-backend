from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    """
    Gerenciador personalizado para o modelo de usuário.

    Responsável por criar usuários e superusuários utilizando o e-mail como identificador principal.
    """
    def create_superuser(self, email, password):
        """
        Cria e retorna um superusuário com o e-mail e senha fornecidos.
        """
        user = self.model(
            email=self.normalize_email(email),
            is_superuser=True
        )
        user.set_password(password)
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    """
    Modelo personalizado de usuário para o sistema.

    Este modelo herda de AbstractUser e permite personalizações adicionais.
    """
    username = None  # Remove o campo username, pois utilizaremos o e-mail como identificador
    avatar = models.TextField(default='media/avatars/default-avatar.png')
    name = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    is_superuser = models.BooleanField(default=False)
    last_access = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    objects = UserManager()

    USERNAME_FIELD = 'email'  # O sistema utilizará o e-mail como campo de autenticação
    REQUIRED_FIELDS = []

    def has_perm(self, perm, obj=None):
        """
        Verifica se o usuário tem permissão para realizar uma ação específica.
        """
        return True

    def has_module_perms(self, app_label):
        """
        Verifica se o usuário tem permissão para acessar um módulo específico.
        """
        return True

    @property
    def is_staff(self):
        """
        Verifica se o usuário é um membro da equipe (staff), por exemplo, fica redundante ter o campo is_staff
        já que o usuário é um superusuário. Se torna uma propriedade para facilitar o acesso.
        """
        return self.is_superuser


    # Classe Meta para definir o nome da tabela no banco de dados
    class Meta:
        db_table = 'users'
        