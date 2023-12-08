import uuid,random
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import AccessToken

def UUID():
    return str(uuid.uuid4())

def Print(*values):
    # Define ANSI color codes
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'  # Reset to default color

    if not len(values):
        print(f'{YELLOW}\n-------------------------------------------------***--------------------------------------------------{RESET}')
        print(f'{GREEN}\n----------------------------------------------Proceed-----------------------------------------------{RESET}')
        print(f'{YELLOW}\n-------------------------------------------------***--------------------------------------------------{RESET}')
        return 0

    for value in values:
        print(f'{YELLOW}\n-------------------------------------------------***--------------------------------------------------{RESET}')
        print(f'value : {GREEN}{value}{RESET}')
        print(f'type : {GREEN}{type(value)}{RESET}')
        print(f'detial : {GREEN}{str(value)}{RESET}')
        try:
            print(f'length : {GREEN}{len(value)}{RESET}')
        except:
            print(f'length : {RED}N/A{RESET}')
        print(f'properties : {GREEN}{dir(value)}{RESET}')
        print(f'{YELLOW}\n-------------------------------------------------***--------------------------------------------------{RESET}')

       
def get_name(obj):
    return obj.first_name + ' ' + obj.last_name
        
def verify_and_get_token_payload(request):
    try:
        auth_header=request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise PermissionDenied('Invalid Authorizaton header')
        token = auth_header.split(' ')[1]
        try:
            access_token = AccessToken(token)
            payload = access_token.payload
            access_token.verify()
            return True, payload
        except Exception as e:
            return False, str(e)
    except Exception as e:
        return False, str(e)


def get_travel_mate_name(travel_mate):
    return travel_mate.first_name + ' ' + travel_mate.last_name


def get_travel_mate_id():
    from TravelMates.models import TravelMate
    travel_mate_id = 0
    old_ids = list(TravelMate.objects.values_list('travel_mate_id',flat=True).distinct())
    while True:
        travel_mate_id = random.randint(5000000000,5999999999)
        if travel_mate_id not in old_ids:
            break
    return str(travel_mate_id)

def get_trip_id():
    from Trips.models import Trip
    trip_id = 0
    old_ids = list(Trip.objects.distinct().values_list('trip_id',flat=True))
    while True:
        trip_id ='trip_'+str(random.randint(5000000000,5999999999))
        if trip_id not in old_ids:
            break
    return str(trip_id)

def get_trip_like_id():
    from Interactions.models import TripLike
    like_id = 0
    old_ids = list(TripLike.objects.values_list('like_id',flat=True).distinct())
    while True:
        like_id ='trip_like_'+str(random.randint(5000000000,5999999999))
        if like_id not in old_ids:
            break
    return str(like_id)

def get_trip_comment_id():
    from Interactions.models import TripComment
    comment_id = 0
    old_ids = list(TripComment.objects.values_list('comment_id',flat=True).distinct())
    while True:
        comment_id ='trip_comment_'+str(random.randint(5000000000,5999999999))
        if comment_id not in old_ids:
            break
    return str(comment_id)

def get_trip_request_id():
    from Interactions.models import TripRequest
    request_id = 0
    old_ids = list(TripRequest.objects.values_list('request_id',flat=True).distinct())
    while True:
        request_id ='trip_request_'+str(random.randint(5000000000,5999999999))
        if request_id not in old_ids:
            break
    return str(request_id)

def get_conversation_id():
    conversation_id ='conversation_'+str(UUID())
    return str(conversation_id)

def get_message_id():
    message_id ='message_'+str(UUID())
    return str(message_id)
