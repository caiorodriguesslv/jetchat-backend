from django.db import models
from accounts.models import User

class Chat(models.Model):
    """
    Representa o chat entre dois usuários.
    """
    from_user = models.ForeignKey(
        User, related_name='Chats_from_user_id', on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        User, related_name='Chats_to_user_id', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chats'
       

class ChatMessage(models.Model):
    """
    Representa uma mensagem dentro de um chat.
    """
    body = models.TextField(null=True)
    attachment_code = models.CharField(
        choices=[('FILE', 'FILE'), ('AUDIO', 'AUDIO')],
        max_length=10, 
        null=True
    )
    attachment_id = models.IntegerField(null=True)
    viewd_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'chat_messages'
        

