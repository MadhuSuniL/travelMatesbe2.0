from TravelMates.models import TravelMate
from django.conf import settings
from helper.Funtions import verify_and_get_token_payload
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from TravelMates.ws_auths_and_funcs import verify_and_get_token_payload_for_ws

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
    
    
@database_sync_to_async
def get_user(travel_mate_id):
    try:
        return TravelMate.objects.get(travel_mate_id = travel_mate_id)
    except TravelMate.DoesNotExist:
        return None

class WSAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    def get_travel_mate(self,travel_mate_id):
        return TravelMate.objects.get(travel_mate_id = travel_mate_id)    
        
    async def __call__(self, scope, receive, send):
        try:
            payload= verify_and_get_token_payload_for_ws(scope)
            travel_mate_id = payload['travel_mate_id']
            travel_mate = await sync_to_async(self.get_travel_mate)(travel_mate_id)
            scope['travel_mate'] = travel_mate
            scope['done'] = True   
            return await self.app(scope, receive, send)
        except Exception as e:    
            scope['travel_mate'] = None
            scope['done'] = False
            scope['msg'] = str(e)
            return await self.app(scope, receive, send)
