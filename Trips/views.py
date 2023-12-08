from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from Trips.serializers import TripSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from Trips.models import Trip
from helper.Funtions import Print
from datetime import datetime

[
    {"label": "Adventure", "value": "adventure"},
    {"label": "Beach Vacation", "value": "beach-vacation"},
    {"label": "Cultural Exploration", "value": "cultural-exploration"},
    {"label": "City Sightseeing", "value": "city-sightseeing"},
    {"label": "Hiking and Nature", "value": "hiking-and-nature"},
    {"label": "Food and Culinary Tours", "value": "food-and-culinary"},
    {"label": "Wellness and Relaxation", "value": "wellness-and-relaxation"},
    {"label": "Wildlife and Safari", "value": "wildlife-and-safari"},
    {"label": "History and Heritage", "value": "history-and-heritage"},
    {"label": "Family-Friendly", "value": "family-friendly"},
    {"label": "Romantic Getaway", "value": "romantic-getaway"},
    {"label": "Ecotourism", "value": "ecotourism"},
    {"label": "Mountain and Skiing", "value": "mountain-and-skiing"},
    {"label": "Island Paradise", "value": "island-paradise"},
    {"label": "Road Trip", "value": "road-trip"},
    {"label": "Cruise and Sailing", "value": "cruise-and-sailing"},
    {"label": "Festivals and Events", "value": "festivals-and-events"},
    {"label": "Volunteering and Community", "value": "volunteering-and-community"},
    {"label": "Art and Architecture", "value": "art-and-architecture"},
    {"label": "Luxury and Spa Retreats", "value": "luxury-and-spa-retreats"},
    {"label": "Scenic Drives", "value": "scenic-drives"},
    {"label": "Solo Travel", "value": "solo-travel"},
    {"label": "Shopping and Markets", "value": "shopping-and-markets"},
    {"label": "Wine and Vineyards", "value": "wine-and-vineyards"},
    {"label": "Backpacking and Budget", "value": "backpacking-and-budget"},
    {"label": "Historical Landmarks", "value": "historical-landmarks"},
    {"label": "Amusement Parks", "value": "amusement-parks"},
    {"label": "Nature Retreat", "value": "nature-retreat"},
    {"label": "Golf and Sports", "value": "golf-and-sports"},
    {"label": "Underwater Exploration", "value": "underwater-exploration"},
    {"label": "Cultural Festivals", "value": "cultural-festivals"},
    {"label": "Roadside Attractions", "value": "roadside-attractions"},
    {"label": "Educational Tours", "value": "educational-tours"},
    {"label": "River Cruises", "value": "river-cruises"},
    {"label": "Music and Entertainment", "value": "music-and-entertainment"},
    {"label": "Yoga and Meditation Retreats", "value": "yoga-and-meditation-retreats"},
    {"label": "Desert Adventures", "value": "desert-adventures"},
    {"label": "Ski Resorts", "value": "ski-resorts"},
    {"label": "Rainforest Expeditions", "value": "rainforest-expeditions"},
    {"label": "Health and Wellness Escapes", "value": "health-and-wellness-escapes"}
]


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
        type_ =  request.GET.get('type')
        if type_:
            current_date = datetime.now()
            travel_mate = request.travel_mate
            if type_ == 'upcoming':
                trips = self.get_queryset().filter(travel_mate = travel_mate, date__gt = current_date)
            else:
                trips = self.get_queryset().filter(travel_mate = travel_mate, date__lt = current_date)
            data = self.get_serializer(trips, many=True).data                
            return Response(data)
        return super().list(request, *args, **kwargs)
         
class TripFilterData(APIView):
    def get(self, request):
        data = {}
        
        titles = Trip.objects.values_list('title', flat=True).distinct()
        departures = Trip.objects.values_list('departure', flat=True).distinct()
        destinations = Trip.objects.values_list('destination', flat=True).distinct()
        categories = Trip.objects.values_list('category', flat=True).distinct()
        
        data['titles'] = titles
        data['departures'] = departures
        data['destinations'] = destinations
        data['categories'] = categories
        
        
        return Response(data)
    
    
    
    