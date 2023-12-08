from django.db import models
from helper.Modals import DateTimeModal
from TravelMates.models import TravelMate


class Conversation(DateTimeModal):
    conversation_id = models.CharField(max_length=50,unique=True)
    from_travel_mate = models.ForeignKey(TravelMate, related_name= 'conversation_from', to_field='travel_mate_id', on_delete= models.CASCADE) 
    to_travel_mate = models.ForeignKey(TravelMate, related_name= 'conversation_to', to_field='travel_mate_id', on_delete= models.CASCADE)
    
    
class Message(DateTimeModal):
    message_id = models.CharField(max_length=50,unique=True)
    conversation = models.ForeignKey(Conversation, to_field='conversation_id', on_delete=models.CASCADE)
    travel_mate = models.ForeignKey(TravelMate, related_name= 'travel_mate_messages', to_field='travel_mate_id', on_delete= models.CASCADE) 
    message = models.TextField()
    is_seen = models.BooleanField(default=False)
        

