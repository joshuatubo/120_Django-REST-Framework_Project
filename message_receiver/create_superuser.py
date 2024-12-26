import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'message_receiver.settings')
django.setup()

from django.contrib.auth.models import User

# Create superuser
if not User.objects.filter(username='receiver_admin').exists():
    User.objects.create_superuser('receiver_admin', 'receiver@example.com', 'admin123')
