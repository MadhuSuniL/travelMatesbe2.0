from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from Interactions.models import TripComment, TripCommentReply
from Interactions.Trips.Comments.serializers import TripCommentSerializer,TripCommentReplySerialiser
from Trips.models import Trip
from helper.Funtions import get_trip_comment_id


class CreateTripComment(CreateAPIView):
    serializer_class = TripCommentSerializer
    queryset = TripComment.objects.all()  
    
    
    
    
class GetTripCommentsView(ListAPIView):
    serializer_class = TripCommentSerializer
    queryset = TripComment.objects.all()
    
    def get(self, request, trip_id, *args, **kwargs):
        if trip_id == 'all' or trip_id is None:            
            trip_comments = self.get_queryset()
            serializer = TripCommentSerializer(trip_comments, many=True, context={'request': request})
            trip_comments_data = serializer.data
            return Response(trip_comments_data)
        trip_comments = self.get_queryset().filter(trip_id = trip_id)
        serializer = TripCommentSerializer(trip_comments, many=True, context={'request': request})
        trip_comments_data = serializer.data
        return Response(trip_comments_data)
    

class CreateReplyToTripComment(CreateAPIView,ListAPIView):
    serializer_class = TripCommentSerializer
    queryset = TripComment.objects.all()
    
    def get(self, request,comment_id , *args, **kwargs):
        reply_comments = TripCommentReply.objects.filter(comment__comment_id=comment_id)
        data = TripCommentReplySerialiser(reply_comments,many = True).data
        return Response(data)

    def post(self, request,comment_id , *args, **kwargs):
        reply = request.data['reply']
        travel_mate = request.travel_mate
        comment = TripComment.objects.get(comment_id = comment_id)
        trip = comment.trip
        reply_comment = TripComment.objects.create(comment_id = get_trip_comment_id(),trip = trip, comment = reply, travel_mate = travel_mate)        
        reply_comment = TripCommentReply.objects.create(comment=comment,reply_comment = reply_comment)
        data = TripCommentReplySerialiser(reply_comment).data
        return Response(data)
        