from django.urls import path
from .views import *

urlpatterns = [
     path('explore_sample_trip_data', ExploreTripSampleData.as_view())
]