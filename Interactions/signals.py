from django.db.models.signals import pre_save
from django.dispatch import receiver
from helper.Funtions import Print
from .models import TripRequest


@receiver(pre_save, sender=TripRequest)
def trip_request_acepted_created(sender, instance, **kwargs):
    print('0')
    if instance.is_accepted:
        instance.trip.connected_travel_mates += 1
        if instance.trip.strength < instance.trip.connected_travel_mates:
            raise Exception('Trip Strength is full!')
        instance.trip.save()
                