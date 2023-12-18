from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from Chats.utils import categorize_messages
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer



class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    lookup_field = 'message_id'
    
    def get_queryset(self):
        query_params = self.request.query_params
        conversation_id = query_params.get('conversation')
        messages = Message.objects.filter(conversation_id=conversation_id).order_by('create_at')
        return messages
    
        
    # def list(self, request, *args, **kwargs):
    #     data = super().list(request, *args, **kwargs).data
    #     messages = [dict(message_data) for message_data in data]
    #     messages = categorize_messages(messages)
    #     print(len(messages['2023-12-09']))
    #     return Response(messages) # super().list(request, *args, **kwargs)

class ConversationViewSet(ModelViewSet):
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.all()
    
    
    def get_queryset(self):
        travel_mate = self.request.travel_mate
        conversations = Conversation.objects.filter(from_travel_mate=travel_mate) | Conversation.objects.filter(to_travel_mate=travel_mate) 
        return conversations


