from django.urls import path
from TravelMates.consumers import TravelMateStatusConsumer

urlpatterns = [
    path('server',TravelMateStatusConsumer.as_asgi()),
]
