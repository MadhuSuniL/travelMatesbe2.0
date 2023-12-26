from rest_framework import serializers
from Chats.models import Message, Conversation
from helper.Funtions import get_conversation_id, get_message_id, get_name
from TravelMates.serializers import TravelMateSerializer
import humanize
from django.utils.timezone import now

class MessageSerializer(serializers.ModelSerializer):
    message_id = serializers.CharField(required=False)    
    travel_mate = serializers.PrimaryKeyRelatedField(queryset=Message.objects.all(), required=False)     
    conversation = serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all(), required=False)     
    message_sent_time = serializers.SerializerMethodField()
    is_self_sender = serializers.SerializerMethodField()

    class Meta:
        model = Message
        exclude = ['id']

    def get_message_sent_time(self, obj):
        travel_mate = self.context['request'].travel_mate
        message_time = obj.create_at
        current_time = now()
        
        # making seen = true
        if travel_mate != obj.travel_mate:
            obj.is_seen = True
            obj.save()        
        return humanize.naturaltime(current_time - message_time)

        
    def get_is_self_sender(self,obj):
        travel_mate = self.context['request'].travel_mate
        if travel_mate == obj.travel_mate:
            return True
        else:
            return False
        
 
    def create(self, validated_data):
        request = self.context['request']
        conversation = request.query_params.get('conversation')
        conversation = Conversation.objects.get(conversation_id=conversation)
        validated_data['message_id'] = get_message_id()
        validated_data['conversation'] = conversation
        validated_data['travel_mate'] = request.travel_mate
        message = Message.objects.create(**validated_data)
        return message
     
class ConversationSerializer(serializers.ModelSerializer):
    conversation_id = serializers.CharField(required=False)  
    travel_mate = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    def get_travel_mate(self,obj):
        travel_mate = self.context['request'].travel_mate
        if travel_mate == obj.to_travel_mate:
            return TravelMateSerializer(obj.from_travel_mate, context = self.context).data
        else:
            return TravelMateSerializer(obj.to_travel_mate, context = self.context).data
      
    def get_last_message(self, obj):
        travel_mate = self.context['request'].travel_mate
        messages = Message.objects.filter(conversation = obj)
        if len(messages):
            last_message = messages.order_by('-create_at').first()
            if last_message.travel_mate == travel_mate:
                return f'You : {last_message.message}'
            return f'{last_message.travel_mate.first_name} : {last_message.message}'      
        return ''      

    class Meta:
        model = Conversation
        exclude = ['id']

    def create(self, validated_data):
        request = self.context['request']
        validated_data['conversation_id'] = get_conversation_id()
        conversation = Conversation.objects.create(**validated_data)
        return conversation    