from rest_framework.views import APIView
from rest_framework.response import Response
from Interactions.models import Interactions, TripRequest
from Interactions.serializers import InteractionsSerializer


class InteractionsView(APIView):
    def get(self, request, *args, **kwargs):
        source = request.GET.get('source')
        if source == 'badge_count':
            interactions_count = Interactions.objects.filter(travel_mate = request.travel_mate, is_seen = False).count()
            request_count = TripRequest.objects.filter(trip__travel_mate = request.travel_mate, is_accepted = False).count()
            final_count = interactions_count + request_count
            return Response({'interactions_count' : interactions_count,'request_count': request_count, 'final_count' : final_count})
        else :
            interactions = Interactions.objects.filter(travel_mate = request.travel_mate, is_seen = False).order_by('-create_at')
            data = InteractionsSerializer(interactions, many = True).data
            interactions.update(is_seen = True)
            return Response(data)