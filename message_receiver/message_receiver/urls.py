"""
URL configuration for message_receiver project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from core.views import (
    ReceivedMessageViewSet, 
    SentMessageViewSet, 
    receive_message, 
    inbox_view,
    message_list,
    message_detail
)

router = DefaultRouter()
router.register(r'received-messages', ReceivedMessageViewSet, basename='received-message')
router.register(r'sent-messages', SentMessageViewSet, basename='sent-message')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inbox_view, name='inbox'),
    path('messages/', message_list, name='message_list'),
    path('messages/<int:message_id>/', message_detail, name='message_detail'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('api/', include(router.urls)),
    path('api/receive-message/', receive_message, name='receive-message'),
    path('api-auth/', include('rest_framework.urls')),
]
