from rest_framework import serializers
from Interactions.models import TripRequest
from helper.Funtions import get_trip_request_id
from TravelMates.models import TravelMate
import humanize
from django.utils.timezone import now


class TripRequestSerializer(serializers.ModelSerializer):
    request_id = serializers.CharField(required=False)
    travel_mate_name = serializers.CharField(required=False)
    trip_name = serializers.CharField(required=False)
    travel_mate = serializers.PrimaryKeyRelatedField(queryset=TravelMate.objects.all(),required = False)
    create_at = serializers.SerializerMethodField()
    

    def get_create_at(self, obj):
        comment_time = obj.create_at
        current_time = now()
        return humanize.naturaltime(current_time - comment_time)


    class Meta:
        model = TripRequest
        fields = '__all__'
        
    def create(self, validated_data):
        validated_data['travel_mate'] = self.context['request'].travel_mate
        validated_data['request_id'] = get_trip_request_id()
        msg = ''
        try:
            trip_request = TripRequest.objects.get(trip = validated_data['trip'],travel_mate = validated_data['travel_mate'])
            msg = 'You have already requested to this trip'
        except TripRequest.DoesNotExist:
            trip_request = TripRequest.objects.create(**validated_data)            
            msg = 'You have requested to this trip'
        return msg

    def to_representation(self, instance):
        if self.context['request'].method == 'POST':
            response_data = {
                "msg": instance,
            }
            return response_data        
        return super().to_representation(instance)