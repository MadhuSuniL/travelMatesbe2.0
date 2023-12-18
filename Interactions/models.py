from collections.abc import Iterable
from django.db import models
from helper.Modals import DateTimeModal
from helper.Funtions import get_travel_mate_name
from TravelMates.models import TravelMate
from Trips.models import Trip


class TripLike(DateTimeModal):
    trip = models.ForeignKey(Trip, to_field = 'trip_id', related_name = 'trip_trip_like',on_delete=models.CASCADE)
    trip_name = models.CharField(max_length=30)
    travel_mate = models.ForeignKey(TravelMate, to_field = 'travel_mate_id', related_name = 'travel_mate_trip_like',on_delete=models.CASCADE)
    travel_mate_name = models.CharField(max_length=30)
    travel_mate_profile = models.URLField(null=True)
    like_id = models.CharField(max_length=30,unique=True)
    
    def save(self,*args, **kwargs):
        if self.travel_mate:
            self.travel_mate_name = get_travel_mate_name(self.travel_mate)
            self.travel_mate_profile = self.travel_mate.profile_pic.url
        if self.trip:
            self.trip_name = self.trip.title
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.trip_name
    

class TripComment(DateTimeModal):
    trip = models.ForeignKey(Trip, to_field = 'trip_id', related_name = 'trip_trip_comment',on_delete=models.CASCADE)
    trip_name = models.CharField(max_length=30)
    travel_mate = models.ForeignKey(TravelMate, to_field = 'travel_mate_id', related_name = 'travel_mate_trip_comment',on_delete=models.CASCADE)
    travel_mate_name = models.CharField(max_length=30)
    travel_mate_profile = models.URLField(null=True)
    comment_id = models.CharField(max_length=30,unique=True)
    comment = models.TextField(null=True)
    
    def save(self,*args, **kwargs):
        if self.travel_mate:
            self.travel_mate_name = get_travel_mate_name(self.travel_mate)
            self.travel_mate_profile = self.travel_mate.profile_pic.url
        if self.trip:
            self.trip_name = self.trip.title
        return super().save(*args, **kwargs)
      
class TripCommentReply(DateTimeModal):
    comment = models.ForeignKey(TripComment,to_field='comment_id',related_name='main_comment',on_delete=models.CASCADE)
    reply_comment = models.ForeignKey(TripComment,to_field='comment_id',related_name='reply_comment',on_delete=models.CASCADE)
        
class TripRequest(DateTimeModal):
    trip = models.ForeignKey(Trip, to_field = 'trip_id', related_name = 'trip_trip_request',on_delete=models.CASCADE)
    trip_name = models.CharField(max_length=30)
    travel_mate = models.ForeignKey(TravelMate, to_field = 'travel_mate_id', related_name = 'travel_mate_trip_request',on_delete=models.CASCADE)
    travel_mate_name = models.CharField(max_length=30)
    travel_mate_profile = models.URLField(null=True)
    request_id = models.CharField(max_length=30,unique=True)
    msg = models.TextField(null=True)
    is_accepted = models.BooleanField(default=False)
    
    def save(self,*args, **kwargs):
        if self.travel_mate:
            self.travel_mate_name = get_travel_mate_name(self.travel_mate)
            self.travel_mate_profile = self.travel_mate.profile_pic.url
        if self.trip:
            self.trip_name = self.trip.title
        return super().save(*args, **kwargs)
    
class Follower(models.Model):
    travel_mate = models.ForeignKey(TravelMate,to_field='travel_mate_id' ,on_delete=models.CASCADE, related_name='following_set')
    travel_mate_name = models.CharField(max_length=30)
    travel_mate_profile = models.URLField(null=True)
    follower = models.ForeignKey(TravelMate,to_field='travel_mate_id' ,on_delete=models.CASCADE, related_name='followers_set')
    follower_name = models.CharField(max_length=30)

    def save(self, *args, **kwargs):
        if self.travel_mate:
            self.travel_mate_name = self.travel_mate.first_name + ' ' + self.travel_mate.last_name
            self.travel_mate_profile = self.travel_mate.profile_pic.url
        if self.follower:
            self.follower_name = self.follower.first_name + ' ' + self.follower.last_name
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.travel_mate.first_name} is followed by {self.follower.first_name}"
    
class Interactions(DateTimeModal):
    type = models.CharField(max_length=50)
    info = models.TextField()
    link = models.CharField(null=True, max_length=50)
    travel_mate = models.ForeignKey(TravelMate,to_field='travel_mate_id' ,on_delete=models.CASCADE, related_name='interactions')
    travel_mate_name = models.CharField(max_length=30)
    interacter_travel_mate = models.ForeignKey(TravelMate,to_field='travel_mate_id' ,on_delete=models.CASCADE, related_name='interactor')
    interacter_travel_mate_name = models.CharField(max_length=30)
    interacter_travel_mate_profile = models.CharField(max_length=200)
    is_seen = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.travel_mate:            
            self.travel_mate_name = self.travel_mate.first_name + ' ' + self.travel_mate.last_name
        if self.interacter_travel_mate:
            self.interacter_travel_mate_name = self.interacter_travel_mate.first_name + ' ' + self.interacter_travel_mate.last_name
            self.interacter_travel_mate_profile = self.interacter_travel_mate.profile_pic.url
        return super().save(*args, **kwargs)
    