from rest_framework import serializers
from .models import FileAttachment, AudioAttachment
from attachments.utils.formatter import Formatter
from django.conf import settings


class FileAttachmentSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo FileAttachment.
    """
    class Meta:
        model = FileAttachment
        fields = '__all__'
        
    def to_representation(self, instance):
        """
        Método para formatar a representação do objeto.
        ela formata o tamanho do arquivo e adiciona a URL completa.
        """
        data = super().to_representation(instance)
        data['size'] = Formatter.format_by_type(instance.size)
        data['src'] = f"{settings.CURRENT_URL}{isntance.src}"

        return data



class AudioAttachmentSerializer(serializers.ModelSerializer):
    """
    Serializador para o modelo FileAttachment.
    """
    class Meta:
        model = AudioAttachment
        fields = '__all__'
        
    def to_representation(self, instance):
        """
        Método para formatar a representação do objeto.
        ele adiciona a URL completa.
        """
        data = super().to_representation(instance)
        data['src'] = f"{settings.CURRENT_URL}{isntance.src}"

        return data
