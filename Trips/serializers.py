from rest_framework import serializers
from Trips.models import Trip
from Interactions.models import TripRequest
from helper.Funtions import Print, get_trip_id
from TravelMates.models import TravelMate
from Interactions.Trips.Likes.views import GetTripLikesView
from Interactions.Trips.Comments.views import GetTripCommentsView
from Interactions.Trips.Requests.views import GetTripRequestsView
from TravelMates.serializers import TravelMateSerializer
import humanize
from django.utils.timezone import now
from Interactions.Trips.Requests.serializers import TripRequestSerializer



class TripSerializer(serializers.ModelSerializer):
    trip_id = serializers.CharField(required=False)    
    travel_mate = serializers.PrimaryKeyRelatedField(queryset=TravelMate.objects.all(), required=False)  # Mark it as not required    travel_mate_name = serializers.CharField(required=False)    
    travel_mate_profile = serializers.SerializerMethodField()
    distance = serializers.IntegerField(required=False)    
    description = serializers.CharField(required=False)
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    requests = serializers.SerializerMethodField()
    connected_travel_mates = serializers.SerializerMethodField()
    is_requested = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    trip_date = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        exclude = ['id']
        
    def get_trip_date(self, obj):
        trip_time = obj.date
        current_time = now()
        return humanize.naturaltime(current_time - trip_time).replace('from now', 'to go')

    def get_travel_mate_profile(self, obj):
        return obj.travel_mate.profile_pic.url
    
    def get_likes(self,obj):
        get_trip_likes = GetTripLikesView()
        likes_data =  get_trip_likes.get(request = self.context['request'], trip_id = obj.trip_id).data
        return likes_data   
        
    def get_comments(self,obj):
        get_trip_comments = GetTripCommentsView()
        commnets_data =  get_trip_comments.get(request = self.context['request'], trip_id = obj.trip_id).data
        return commnets_data   
        
    def get_requests(self,obj):
        get_trip_requests = TripRequest.objects.filter(trip = obj)
        requests_data =  TripRequestSerializer(get_trip_requests, many = True, context = self.context).data
        return requests_data   
        
    def get_connected_travel_mates(self,obj):
        requests_travel_mates_id = TripRequest.objects.filter(trip = obj ,is_accepted = True).values_list('travel_mate',flat=True)
        connected_travel_mates_data = TravelMateSerializer(TravelMate.objects.filter(travel_mate_id__in = requests_travel_mates_id),many=True, context = self.context).data
        return connected_travel_mates_data
    
    def get_is_requested(self,obj):
        value = False
        requests = [dict(item) for item in self.get_requests(obj)]
        current_travel_mate_id = self.context['request'].travel_mate.travel_mate_id
        for request in requests:
            if request['travel_mate'] == current_travel_mate_id:
                value = True
        return value

    def get_is_liked(self,obj):
        value = False
        likes = [dict(item) for item in self.get_likes(obj)]
        current_travel_mate_id = self.context['request'].travel_mate.travel_mate_id
        for like in likes:
            if like['travel_mate'] == current_travel_mate_id:
                value = True
        return value

    def get_is_following(self,obj):
        value = False
        requests = [dict(item) for item in self.get_requests(obj)]
        current_travel_mate_id = self.context['request'].travel_mate.travel_mate_id
        for request in requests:
            if request['travel_mate'] == current_travel_mate_id:
                value = True
        return False
    
    def create(self, validated_data):
        request = self.context['request']
        validated_data['trip_id'] = get_trip_id()
        validated_data['travel_mate'] = request.travel_mate
        print(validated_data)
        trip = Trip.objects.create(**validated_data)
        return trip    
    