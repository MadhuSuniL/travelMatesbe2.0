from rest_framework.response import Response
from rest_framework.views import APIView
from helper.Funtions import Print
from Explore.models import TripSample


class ExploreTripSampleData(APIView):
    def get(self, request):
        import requests
        url = 'https://travelmates.pythonanywhere.com/explore/trips/all'
        trip_sample_data = requests.get(url).json()  
        for trip_sample in trip_sample_data:
            modal_data = {
                'title': trip_sample['title'],
                'content': trip_sample['content'],
                'image_url': trip_sample['image'],
                'category': trip_sample['contry'],
            }
            TripSample.objects.create(**modal_data)                                        
        return Response('Fake Data is available now for Explore Trip Sample')