from rest_framework import serializers
from Interactions.models import TripLike
from helper.Funtions import get_trip_like_id, Print
from TravelMates.models import TravelMate

class TripLikeSerializer(serializers.ModelSerializer):
    like_id = serializers.CharField(required=False)
    travel_mate_name = serializers.CharField(required=False)
    travel_mate = serializers.PrimaryKeyRelatedField(queryset=TravelMate.objects.all(),required = False)
    trip_name = serializers.CharField(required=False)
    
    class Meta:
        model = TripLike
        fields = '__all__'
        
    def create(self, validated_data):
        validated_data['travel_mate'] = self.context['request'].travel_mate
        validated_data['like_id'] = get_trip_like_id()
        is_liked = False
        try:
            trip_like = TripLike.objects.get(trip = validated_data['trip'],travel_mate = validated_data['travel_mate'])
            trip_like.delete() 
            is_liked = False
        except TripLike.DoesNotExist:
            trip_like = TripLike.objects.create(**validated_data)
            is_liked = True
        except Exception as e:
            raise e
        return is_liked
    
    def to_representation(self, instance):
        if self.context['request'].method == 'POST':
            response_data = {
                "is_liked": instance,
            }
            return response_data
        return super(TripLikeSerializer, self).to_representation(instance)