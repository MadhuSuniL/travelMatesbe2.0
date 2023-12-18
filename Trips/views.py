from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from Trips.serializers import TripSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from Trips.models import Trip
from helper.Funtions import create_interaction, Print
from datetime import datetime


class TripViewSet(ModelViewSet):
    serializer_class = TripSerializer
    queryset = Trip.objects.all()
    lookup_field = 'trip_id'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('title', 'departure','destination','category','date','strength','distance')
    search_fields = ('title', 'departure','destination','category')
    
    # def get_queryset(self):
    #     travel_mate = self.request.travel_mate
    #     return super().get_queryset().filter(travel_mate = travel_mate)
    
         
    def list(self, request, *args, **kwargs):
        travel_mate_id = request.GET.get('travel_mate_id')
        type_ =  request.GET.get('type')
        if type_:
            current_date = datetime.now()
            if type_ == 'upcoming':
                trips = self.get_queryset().filter(travel_mate_id = travel_mate_id, date__gt = current_date)
            else:
                trips = self.get_queryset().filter(travel_mate_id = travel_mate_id, date__lt = current_date)
            data = TripSerializer(trips, many=True, context = {'request':request}).data                
            return Response(data)
        
        trips = Trip.objects.exclude(travel_mate = request.travel_mate)
        data = TripSerializer(trips, many=True, context = {'request':request}).data                
        return Response(data)
    
class TripFilterData(APIView):
    def get(self, request):
        data = {}
        
        titles = Trip.objects.exclude(travel_mate = request.travel_mate).values_list('title', flat=True).distinct()
        departures = Trip.objects.exclude(travel_mate = request.travel_mate).values_list('departure', flat=True).distinct()
        destinations = Trip.objects.exclude(travel_mate = request.travel_mate).values_list('destination', flat=True).distinct()
        categories = Trip.objects.exclude(travel_mate = request.travel_mate).values_list('category', flat=True).distinct()
        
        data['titles'] = titles
        data['departures'] = departures
        data['destinations'] = destinations
        data['categories'] = categories
        
        
        return Response(data)
    
    
    
    