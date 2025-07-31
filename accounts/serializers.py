from rest_framework import serializers
from django.conf import settings
from accounts.models import User

# Serializador para o modelo User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'avatar', 'last_access']
        read_only_fields = ['id']

    def to_representation(self, instance):
        """
        Customiza a representação do usuário para incluir o avatar completo.
        """
        data = super().to_representation(instance)
        data['avatar'] = f"{settings.CURRENT_URL}{instance.avatar}" 

        return data