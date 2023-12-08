
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from Interactions.Trips.Likes.serializers import TripLikeSerializer
from Interactions.models import TripLike
from helper.Funtions import Print


class CreateTripLike(CreateAPIView):
    serializer_class = TripLikeSerializer
    queryset = TripLike.objects.all()    
    
class GetTripLikesView(ListAPIView):
    serializer_class = TripLikeSerializer
    queryset = TripLike.objects.all()
    
    def get(self, request, trip_id, *args, **kwargs):
        if trip_id == 'all' or trip_id is None:            
            trip_likes = self.get_queryset()
            serializer = TripLikeSerializer(trip_likes, many=True, context={'request': request})
            likes_data = serializer.data
            return Response(likes_data)
        trip_likes = self.get_queryset().filter(trip_id = trip_id)
        serializer = TripLikeSerializer(trip_likes, many=True, context={'request': request})
        likes_data = serializer.data
        return Response(likes_data)
    
