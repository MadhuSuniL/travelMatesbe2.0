from TravelMates.models import TravelMate
from django.conf import settings
from helper.Funtions import verify_and_get_token_payload

class TravelMateRequestMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.travel_mate=None
        # for anonymous paths
        if request.path in settings.ANONYMOUS_PATHS:
                print(request.path)
                response = self.get_response(request)
                a=response.__dict__
                return response        
        else:
            # Checking auth for user paths
            status, payload= verify_and_get_token_payload(request)
            try:
                if status:
                    request.travel_mate=TravelMate.objects.get(travel_mate_id = payload['travel_mate_id'])
            except Exception as e:
                print('EXC @ Middleware:', e)
            response = self.get_response(request)
            
            a=response.__dict__
            return response
    