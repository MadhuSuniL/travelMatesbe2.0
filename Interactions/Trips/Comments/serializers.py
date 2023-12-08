from rest_framework import serializers
from Interactions.models import TripComment, TripCommentReply
from helper.Funtions import get_trip_comment_id, Print
from TravelMates.models import TravelMate
from datetime import datetime, timedelta
import humanize
from django.utils.timezone import now

class TripCommentSerializer(serializers.ModelSerializer):
    comment_id = serializers.CharField(required=False)
    travel_mate = serializers.PrimaryKeyRelatedField(queryset=TravelMate.objects.all(),required = False)
    travel_mate_name = serializers.CharField(required=False)
    trip_name = serializers.CharField(required=False)
    replies = serializers.SerializerMethodField()
    create_at = serializers.SerializerMethodField()
    

    def get_create_at(self, obj):
        comment_time = obj.create_at
        current_time = now()
        return humanize.naturaltime(current_time - comment_time)
    
    def get_replies(self, obj):
        from Interactions.Trips.Comments.views import CreateReplyToTripComment
        reply_comments = CreateReplyToTripComment()
        reply_comments_data = reply_comments.get(request = self.context.get('request'), comment_id = obj.comment_id).data
        return [reply['reply_comment'] for reply in reply_comments_data]
    
    class Meta:
        model = TripComment
        fields = '__all__'
        
    def create(self, validated_data):
        validated_data['travel_mate'] = self.context['request'].travel_mate
        validated_data['comment_id'] = get_trip_comment_id()
        return super().create(validated_data)    


class TripCommentReplySerialiser(serializers.ModelSerializer):
    reply_comment = TripCommentSerializer()
    class Meta:
        model = TripCommentReply
        exclude = ['id']
        