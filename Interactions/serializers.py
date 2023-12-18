from rest_framework import serializers
from Interactions.models import Interactions


class InteractionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interactions
        fields = '__all__'
        
        