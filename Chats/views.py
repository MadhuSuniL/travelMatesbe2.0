from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer



class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    
    def get_queryset(self):
        query_params = self.request.query_params
        conversation_id = query_params.get('conversation')
        messages = Message.objects.filter(conversation_id=conversation_id)
        return messages
    
    # def get(self,request, *args, **kwargs):
    #     travel_mate = request.travel_mate
    #     conversation = request.qury_params.get('conversation')
    #     messeges = Message.objects.filter(conversation_id=conversation).exclude(travel_mate = travel_mate)
    #     print(messeges)
    #     messeges.update(is_seen=True)        
    #     return super().get(request, *args, **kwargs)

class ConversationViewSet(ModelViewSet):
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.all()
    
    
    def get_queryset(self):
        travel_mate = self.request.travel_mate
        conversations = Conversation.objects.filter(from_travel_mate=travel_mate) | Conversation.objects.filter(to_travel_mate=travel_mate) 
        return conversations


