from rest_framework import serializers
from TravelMates.models import TravelMate
from helper.email import welcome, welcome_wtih_credentials
from Interactions.models import Follower


class TravelMateSerializer(serializers.ModelSerializer):
    travel_mate_id = serializers.CharField(allow_blank=True, required=False)
    password = serializers.CharField(write_only=True)
    is_following = serializers.SerializerMethodField()
    email_sent = serializers.BooleanField(default=False)

    class Meta:
        model = TravelMate
        exclude = ['is_active','is_verified','is_staff','id']
        
        
    def get_is_following(self,obj):
        travel_mate = self.context['request'].travel_mate
        followers = Follower.objects.filter(travel_mate_id=obj.travel_mate_id, follower = travel_mate)
        if len(followers):
            return True
        return False
    
    def validate(self, attrs):
        return super().validate(attrs)
    
    def create(self, validated_data):
        email_sent = validated_data.get('email_sent', False)
        del validated_data['email_sent']
        travel_mate = TravelMate.objects.create_travel_mate(**validated_data)
        try:
            if email_sent:
                welcome_wtih_credentials(travel_mate.first_name, travel_mate.email, validated_data['phone'], validated_data['password'])
            else:        
                welcome(travel_mate.first_name, travel_mate.email)
        except:
            pass
        return travel_mate
    
