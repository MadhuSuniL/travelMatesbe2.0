from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from Interactions.models import TripRequest
from Interactions.Trips.Requests.serializers import TripRequestSerializer


class CreateTripRequest(CreateAPIView):
    serializer_class = TripRequestSerializer
    queryset = TripRequest.objects.all()  
    
    
    
class GetTripRequestsView(ListAPIView):
    serializer_class = TripRequestSerializer
    queryset = TripRequest.objects.all()
    
    def get(self, request, trip_id, *args, **kwargs):
        if trip_id == 'all' or trip_id is None:            
            trip_requests = self.get_queryset()
            serializer = TripRequestSerializer(trip_requests, many=True, context={'request': request})
            trip_requests_data = serializer.data
            return Response(trip_requests_data)
        trip_requests = self.get_queryset().filter(trip_id = trip_id)
        serializer = TripRequestSerializer(trip_requests, many=True, context={'request': request})
        trip_requests_data = serializer.data
        return Response(trip_requests_data)
    
class TripRequestAcceptView(RetrieveAPIView):
    serializer_class = TripRequestSerializer
    queryset = TripRequest.objects.filter(is_accepted=False)
    
    def get(self, request, request_id):
        trip_request = self.get_queryset().get(request_id = request_id)
        trip_request.is_accepted = True
        trip_request.save()
        return Response({'detial':'Trip requested successfully'})
    