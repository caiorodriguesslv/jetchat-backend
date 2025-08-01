from django.db import models



class FileAttachment(models.Model):
    """
    Modelo para armazenar arquivos anexados.
    """
    file = models.FileField(upload_to='attachments/')
    name = models.CharField(max_length=90)
    extension = models.CharField(max_length=10)
    size = models.FloatField()
    src = models.TextField()
    content_type = models.CharField(max_length=45)

    class Meta:
        db_table = 'file_attachments'

    
class AudioAttachment(models.Model):
    """
    Modelo para armazenar arquivos de áudio anexados.
    """
    file = models.FileField(upload_to='audio_attachments/')
    src = models.TextField()

    class Meta:
        db_table = 'audio_attachments'

