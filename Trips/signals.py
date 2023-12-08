from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Trip


@receiver(post_save, sender=Trip)
def trip_created(sender, instance, created, **kwargs):
    if created:
        travel_mate = instance.travel_mate
        travel_mate.trips += 1
        travel_mate.save()
        