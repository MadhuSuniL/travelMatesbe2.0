from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from Interactions.models import Follower
from TravelMates.models import TravelMate
from TravelMates.serializers import TravelMateSerializer
from helper.Funtions import create_interaction, Print
from Interactions.Trips.Follow.serializers import FollowerSerializer, FollowingSerializer

class FollowView(APIView):
    def get(self, request, travel_mate_id):
        travel_mate = TravelMate.objects.get(travel_mate_id = travel_mate_id) 
        current_travel_mate = request.travel_mate
        if not Follower.objects.filter(travel_mate = travel_mate, follower = current_travel_mate).count():
            Follower.objects.create(travel_mate = travel_mate, follower = current_travel_mate)
            create_interaction({
            'type' : 'follow',
            'travel_mate' : travel_mate,
            'link' : f'/profile/{current_travel_mate.travel_mate_id}',
            'interacter_travel_mate' :current_travel_mate,
        },'following')
            travel_mate.followers += 1
            travel_mate.save()
            current_travel_mate.followings += 1
            current_travel_mate.save()
            return Response({'detail':'Following'})    
        Follower.objects.get(travel_mate = travel_mate, follower = current_travel_mate).delete()
        create_interaction({
            'type' : 'follow',
            'travel_mate' : current_travel_mate,
            'link' : f'/profile/{travel_mate.travel_mate_id}',
            'interacter_travel_mate' : travel_mate,
        },'unfollowing')
        travel_mate.followers -= 1
        travel_mate.save()
        current_travel_mate.followings -= 1
        current_travel_mate.save()
        return Response({'detail':'Unfollowing'})    
    
    
class GetTravelMateFollowers(ListAPIView):
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all()
    
    def get(self, request, travel_mate_id):
        travel_mate = TravelMate.objects.get(travel_mate_id=travel_mate_id)
        followers = Follower.objects.filter(travel_mate=travel_mate)
        data = self.get_serializer(followers, many=True).data
        data = [data['follower'] for data in data]
        return Response(data)        

class GetTravelMateFollowings(ListAPIView):
    serializer_class = FollowingSerializer
    queryset = Follower.objects.all()
    
    def get(self, request, travel_mate_id):
        travel_mate = TravelMate.objects.get(travel_mate_id=travel_mate_id)
        followers = Follower.objects.filter(follower=travel_mate)
        data = self.get_serializer(followers, many=True).data
        data = [data['travel_mate'] for data in data]
        return Response(data)        
