from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ReceivedMessage(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    sender_email = models.EmailField()
    encrypted_content = models.TextField()
    decrypted_content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    original_message_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Message from {self.sender_email} to {self.receiver.email}"

    class Meta:
        ordering = ['-timestamp']

class SentMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages_receiver')
    receiver_email = models.EmailField()
    content = models.TextField()
    encrypted_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"Message to {self.receiver_email} from {self.sender.email}"

    class Meta:
        ordering = ['-timestamp']
