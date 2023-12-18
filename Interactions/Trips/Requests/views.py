from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response
from Interactions.models import TripRequest
from Interactions.Trips.Requests.serializers import TripRequestSerializer
from Chats.models import Conversation
from helper.Funtions import create_interaction, get_conversation_id


class CreateTripRequest(CreateAPIView):
    serializer_class = TripRequestSerializer
    queryset = TripRequest.objects.all()  
    
    
    
class GetTripRequestsView(ListAPIView):
    serializer_class = TripRequestSerializer
    queryset = TripRequest.objects.all()
    
    
    def get(self, request, trip_id, *args, **kwargs):
        travel_mate = request.travel_mate          
        if trip_id == 'all' or trip_id is None:  
            trip_requests = TripRequest.objects.filter(trip__travel_mate = travel_mate, is_accepted = False).order_by('-create_at')
            serializer = TripRequestSerializer(trip_requests, many=True, context={'request': request})
            trip_requests_data = serializer.data
            return Response(trip_requests_data)
        trip_requests = TripRequest.objects.filter(trip_id = trip_id, is_accepted = False).order_by('-create_at')
        serializer = TripRequestSerializer(trip_requests, many=True, context={'request': request})
        trip_requests_data = serializer.data
        return Response(trip_requests_data)
    
class TripRequestAcceptView(RetrieveAPIView):
    serializer_class = TripRequestSerializer
    queryset = TripRequest.objects.filter(is_accepted=False)
    
    def get(self, request, request_id):
        travel_mate = request.travel_mate
        trip_request = self.get_queryset().get(request_id = request_id)
        trip_request.is_accepted = True
        create_interaction({
            'type' : 'request',
            'travel_mate' : trip_request.trip.travel_mate,
            'interacter_travel_mate' : travel_mate,
        },trip_request.trip.title,'accepted')
        trip_request.save()
        # create conversation
        conversations = Conversation.objects.filter(from_travel_mate = travel_mate, to_travel_mate = trip_request.travel_mate) | Conversation.objects.filter(from_travel_mate = trip_request.travel_mate, to_travel_mate = travel_mate)
        if conversations.count() != 0:
            pass
        else:
            Conversation.objects.create(conversation_id=get_conversation_id(),from_travel_mate = travel_mate, to_travel_mate = trip_request.travel_mate)
        return Response({'detial':'Trip accepted successfully'})
    
class DeleteRequest(DestroyAPIView):
    serializer_class = TripRequestSerializer
    queryset = TripRequest.objects.filter(is_accepted=False)
    lookup_field = 'request_id'
    