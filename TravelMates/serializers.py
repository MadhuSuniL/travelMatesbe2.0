from rest_framework import serializers
from TravelMates.models import TravelMate
from helper.email import welcome


class TravelMateSerializer(serializers.ModelSerializer):
    travel_mate_id = serializers.CharField(allow_blank=True, required=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = TravelMate
        exclude = ['is_active','is_verified','is_staff','id']
        
    def create(self, validated_data):
        travel_mate = TravelMate.objects.create_travel_mate(**validated_data)
        # welcome(travel_mate.first_name, travel_mate.email)
        return travel_mate
    
    # def to_representation(self, instance):
    #     from Interactions.Trips.Follow.views import GetTravelMateFollowers
    #     view = self.context.get('view')
    #     if isinstance(view, GetTravelMateFollowers):
    #         excluded_fields = ['field1', 'field2']  # Replace with the fields you want to exclude
    #         for field in excluded_fields:
    #             self.fields.pop(field, None)

    #     return super().to_representation(instance)