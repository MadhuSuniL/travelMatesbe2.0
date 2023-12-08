from rest_framework import serializers
from Interactions.models import Follower
from TravelMates.serializers import TravelMateSerializer

class FollowerSerializer(serializers.ModelSerializer):
    follower = TravelMateSerializer(context = {'f':'f'})    
    
    class Meta:
        model = Follower
        fields = ['follower']

class FollowingSerializer(serializers.ModelSerializer):
    travel_mate = TravelMateSerializer(context = {'f':'f'})    
    travel_mate_name = serializers.CharField()

    class Meta:
        model = Follower
        fields = ['travel_mate','travel_mate_name']

