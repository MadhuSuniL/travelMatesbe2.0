from collections.abc import Iterable
from django.db import models
from helper.Modals import DateTimeModal
from TravelMates.models import TravelMate
from helper.Funtions import get_travel_mate_name



class Trip(DateTimeModal):
    title = models.CharField(max_length=30)
    departure = models.CharField(max_length=30)
    destination = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    date = models.DateTimeField()
    strength = models.IntegerField(default=3)    
    # Optional 
    distance = models.IntegerField(default=None, null=True)    
    description = models.TextField(null=True)
    travel_mate_name = models.CharField(null=True,max_length=30)    
    # readonly
    connected_travel_mates = models.IntegerField(default=0)
    trip_id = models.CharField(unique=True,max_length=100)
    travel_mate = models.ForeignKey(TravelMate,to_field='travel_mate_id',on_delete=models.CASCADE,related_name='travel_mate_trips')

    def __str__(self):
        return self.title    
    
    def save(self, *args, **kwargs):
        if self.travel_mate:
            self.travel_mate_name = get_travel_mate_name(self.travel_mate)
        return super().save(*args, **kwargs)
    
    