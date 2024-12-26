from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver_email', 'content', 'encrypted_content', 'timestamp', 'is_read')
        read_only_fields = ('sender', 'encrypted_content', 'timestamp', 'is_read')
