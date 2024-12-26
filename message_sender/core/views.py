from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Message
from .serializers import UserSerializer, MessageSerializer
from .middleware import EncryptionMiddleware
import requests
from django.utils import timezone
from django.shortcuts import get_object_or_404

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def mark_message_as_read(request):
    try:
        message_id = request.data.get('message_id')
        receiver_email = request.data.get('receiver_email')
        
        message = get_object_or_404(Message, id=message_id, receiver_email=receiver_email)
        message.is_read = True
        message.read_timestamp = timezone.now()
        message.save()
        
        return Response({
            'status': 'success',
            'message': 'Message marked as read'
        })
    except Message.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Message not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user)

    def perform_create(self, serializer):
        try:
            # Create message with encrypted content
            encryption = EncryptionMiddleware(None)
            content = serializer.validated_data['content']
            encrypted_content = encryption.encrypt_message(content)
            
            message = serializer.save(
                sender=self.request.user,
                encrypted_content=encrypted_content
            )

            # Send message to receiver application
            receiver_url = 'http://localhost:8001/api/receive-message/'
            payload = {
                'sender_email': self.request.user.email,
                'receiver_email': message.receiver_email,
                'encrypted_content': encrypted_content,
                'content': content  # Include original content for debugging
            }
            
            print(f"Sending message to receiver: {payload}")
            
            response = requests.post(
                receiver_url,
                json=payload,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                print(f"Message sent successfully: {response.json()}")
            else:
                print(f"Error sending message: {response.text}")
                raise Exception(f"Failed to deliver message: {response.text}")
                
        except Exception as e:
            print(f"Error sending message: {str(e)}")
            raise

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return Response({
                'status': 'Message sent successfully',
                'data': response.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        messages = self.get_queryset()
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
