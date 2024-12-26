from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import ReceivedMessage, SentMessage
from .serializers import ReceivedMessageSerializer, SentMessageSerializer
from django.shortcuts import get_object_or_404, render
from .middleware import DecryptionMiddleware
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import requests
from django.utils import timezone

@login_required
def inbox_view(request):
    received_messages = ReceivedMessage.objects.filter(receiver=request.user).order_by('-timestamp')
    sent_messages = SentMessage.objects.filter(sender=request.user).order_by('-timestamp')
    unread_count = received_messages.filter(is_read=False).count()
    
    return render(request, 'core/inbox.html', {
        'received_messages': received_messages,
        'sent_messages': sent_messages,
        'unread_count': unread_count
    })

@login_required
def message_list(request):
    received_messages = ReceivedMessage.objects.filter(receiver=request.user).order_by('-timestamp')
    sent_messages = SentMessage.objects.filter(sender=request.user).order_by('-timestamp')
    
    return render(request, 'core/message_list.html', {
        'received_messages': received_messages,
        'sent_messages': sent_messages
    })

@login_required
def message_detail(request, message_id):
    message = get_object_or_404(
        ReceivedMessage, 
        id=message_id, 
        receiver=request.user
    )
    
    if not message.is_read:
        message.is_read = True
        message.save()
        
        # Notify sender application that message was read
        try:
            sender_url = 'http://localhost:8000/api/mark-read/'
            response = requests.post(
                sender_url,
                json={
                    'message_id': message.original_message_id,
                    'receiver_email': request.user.email,
                    'timestamp': timezone.now().isoformat()
                }
            )
            print(f"Notified sender of read status: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error notifying sender: {str(e)}")
    
    return render(request, 'core/message_detail.html', {
        'message': message
    })

@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def receive_message(request):
    try:
        print("=== Received Message Request ===")
        print(f"Request method: {request.method}")
        print(f"Request headers: {request.headers}")
        print(f"Request data: {request.data}")
        
        data = request.data
        
        # Find or create receiver user
        try:
            receiver = User.objects.get(email=data['receiver_email'])
        except User.DoesNotExist:
            username = data['receiver_email'].split('@')[0]
            receiver = User.objects.create_user(
                username=username,
                email=data['receiver_email'],
                password='defaultpassword123'
            )
            print(f"Created new user: {username}")
        
        # Decrypt the message and verify integrity
        decryption = DecryptionMiddleware(None)
        try:
            decrypted_content = decryption.decrypt_message(data['encrypted_content'])
            print(f"Successfully decrypted message with integrity check")
        except Exception as e:
            print(f"Decryption or integrity check failed: {str(e)}")
            return Response({
                'error': 'Message decryption or integrity check failed',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the message
        message = ReceivedMessage.objects.create(
            receiver=receiver,
            sender_email=data['sender_email'],
            encrypted_content=data['encrypted_content'],
            decrypted_content=decrypted_content,
            is_read=False,
            original_message_id=data.get('message_id'),
            timestamp=data.get('timestamp') or timezone.now()
        )
        
        print(f"Secure message created and stored: {message}")
        return Response({
            'status': 'Message received and verified',
            'message_id': message.id
        }, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Error processing encrypted message: {str(e)}")
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

class ReceivedMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ReceivedMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ReceivedMessage.objects.filter(receiver=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        message = self.get_object()
        if not message.is_read:
            message.is_read = True
            message.save()
            
            # Notify sender application
            try:
                sender_url = 'http://localhost:8000/api/mark-read/'
                response = requests.post(
                    sender_url,
                    json={
                        'message_id': message.original_message_id,
                        'receiver_email': request.user.email,
                        'timestamp': timezone.now().isoformat()
                    }
                )
                print(f"Notified sender of read status: {response.status_code} - {response.text}")
            except Exception as e:
                print(f"Error notifying sender: {str(e)}")
                
        return Response({'status': 'message marked as read'})

class SentMessageViewSet(viewsets.ModelViewSet):
    serializer_class = SentMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SentMessage.objects.filter(sender=self.request.user)

    def perform_create(self, serializer):
        try:
            from .middleware import DecryptionMiddleware
            encryption = DecryptionMiddleware(None)
            content = serializer.validated_data['content']
            encrypted_content = encryption.encrypt_message(content)
            
            message = serializer.save(
                sender=self.request.user,
                encrypted_content=encrypted_content
            )

            # Send message to sender application
            sender_url = 'http://localhost:8000/api/receive-message/'
            response = requests.post(
                sender_url,
                json={
                    'sender_email': self.request.user.email,
                    'receiver_email': message.receiver_email,
                    'encrypted_content': encrypted_content,
                    'content': content,  # Include original content for debugging
                    'message_id': message.id  # Include the original message ID
                }
            )
            
            if response.status_code == 200:
                message.is_delivered = True
                message.save()
            
            return Response({
                'status': 'Message sent',
                'message_id': message.id
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
