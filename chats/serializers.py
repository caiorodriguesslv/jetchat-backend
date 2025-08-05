from rest_framework import serializers

from accounts.serializers import UserSerializer

from chats.models import Chat, ChatMessage

from attachaments.models import Attachment, AttachmentSerializer
from attachments.serializers import FileAttachmentSerializer, AudioAttachmentSerializer


class ChatSerializer(serializers.ModelSerializer):
    """ 
    Serializador para o modelo Chat. 
    Inclui informações do usuário, contagem de mensagens não lidas e última mensagem.
    """
    user = serializers.SerializerMethodField()
    unseen_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['id', 'viewed_at', 'created_at', 'user', 'unseen_count', 'last_message']

    def get_user(self, chat):
        user = chat.from_user

        # Checa se o usuário atual é o remetente do chat
        if user.id == self.context['user_id']:
            user = chat.to_user

        return UserSerializer(user).data

    def get_unseen_count(self, chat):
        """ 
        Retorna a contagem de mensagens não lidas no chat
        Ela verifica se a mensagem pertence ao chat, se não foi visualizada,
        se não foi deletada e se não é do usuário atual.   
        """
        unseen_count = chat.objects.filter(
            chat_id=chat.id, # Verifica se a mensagem pertence ao chat
            viewed_at__isnull=True, # Verifica se a mensagem não foi visualizada
            deleted_at__isnull=True, # Verifica se a mensagem não foi deletada
            from_user__id__ne=self.context['user_id'] # Verifica se a mensagem não é do usuário atual
        ).exclude(
            from_user=self.context['user_id'] # Exclui mensagens enviadas pelo usuário atual
        ).count()

    def last_message(self, chat):
        """ 
        Retorna a última mensagem do chat.
        Se não houver mensagens, retorna None.
        """
        last_message = chat.chatmessage_set.objects.filter(
            chat_id=chat.id,
            deleted_at__isnull=True
        ).order_by('-created_at').first() # Ordena por data de criação e pega a última mensagem

        if not last_message:
            return None

        return ChatMessageSerializer(last_message, self.context)

    
class ChatMessageSerializer(serializers.ModelSerializer):
    """ 
    Serializador para o modelo ChatMessage. 
    Inclui informações do usuário e do anexo, se houver.
    """
    from_user = UserSerializer()
    attachment = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = ['id', 'body', 'viewed_at', 'created_at', 'from_user', 'attachment']

    def get_from_user(self, chat_message):
        """ Retorna o usuário que enviou a mensagem. """
        return UserSerializer(chat_message.from_user).data

    def get_attachment(self, chat_message):
        """
        Retorna o anexo da mensagem, se houver.
        Se o anexo for do tipo 'FILE', usa FileAttachmentSerializer.
        Se for do tipo 'AUDIO', usa AudioAttachmentSerializer.
        """

        # Verifica se a mensagem tem um anexo do tipo 'FILE'
        if chat_message.attachment_code == 'FILE':
            file_attachment = FileAttachment.objects.filter(
                id=chat_message.attachment_id,
                attachment_code='FILE'
            ).first()
            
            if not file_attachment:
                return None

            return {
                "file": FileAttachmentSerializer(file_attachment).data
            }

        # Verifica se a mensagem tem um anexo do tipo 'AUDIO'
        if chat_message.attachment_code == 'AUDIO':
            audio_attachment = AudioAttachment.objects.filter(
                id=chat_message.attachment_id,
                attachment_code='AUDIO'
            ).first()
            
            if not audio_attachment:
                return None

            return {
                "audio": AudioAttachmentSerializer(audio_attachment).data
            }

        return None