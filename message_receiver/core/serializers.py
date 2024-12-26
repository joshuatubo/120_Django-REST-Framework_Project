from rest_framework import serializers
from .models import ReceivedMessage, SentMessage
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class ReceivedMessageSerializer(serializers.ModelSerializer):
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = ReceivedMessage
        fields = ('id', 'receiver', 'sender_email', 'encrypted_content', 'decrypted_content', 'timestamp', 'is_read')

class SentMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = SentMessage
        fields = ('id', 'sender', 'receiver_email', 'content', 'encrypted_content', 'timestamp', 'is_delivered')
        read_only_fields = ('sender', 'encrypted_content', 'timestamp', 'is_delivered')
