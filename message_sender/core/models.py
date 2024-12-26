from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver_email = models.EmailField()
    content = models.TextField()
    encrypted_content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_delivered = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    read_timestamp = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver_email}"

    class Meta:
        ordering = ['-timestamp']
