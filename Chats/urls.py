from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

default_router = DefaultRouter()
default_router.register('message', MessageViewSet)
default_router.register('conversation', ConversationViewSet)

urlpatterns = [
    path('', include(default_router.urls))
]