from django.db import models


# Create your models here.
class Message(models.Model):
    sequence_id = models.AutoField(verbose_name="聊天记录ID", max_length=8, primary_key=True)
    from_id = models.CharField(verbose_name='发送者id',max_length=8)
    to_id = models.CharField(verbose_name='接受者id',max_length=8)
    chat_send_time = models.DateTimeField(verbose_name='发送时间',auto_now=True)
    chat_content = models.TextField(verbose_name='私信内容')

    def __str__(self):
        return self.sequence_id

    class Meta:
        db_table = 'tb_message'
