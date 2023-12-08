from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('trips',TripViewSet)


urlpatterns = [
    path('',include(router.urls)),
    path('trips/filter_data_keys',TripFilterData.as_view())
]