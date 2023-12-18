from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,UpdateAPIView
from rest_framework.response import Response
from helper.Funtions import Print
from helper.email import password_change
from .models import Otp, TravelMate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import TravelMateSerializer
from helper.ViewHandlers import CustomViewHandler
from django.utils import timezone
import random

class LoginView(CustomViewHandler,APIView):
    
    authentication_classes = []
    permission_classes = []
    
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        password = request.data.get('password')
        if not (phone and password):
            raise Exception('Blank phone or password')
        travel_mate = TravelMate.objects.authenticate(phone=phone, password=password)
        if not travel_mate:
            raise Exception('Incorrect phone number or password')
        travel_mate.last_login = timezone.now()
        travel_mate.save()
        refresh = RefreshToken.for_user(travel_mate)
        refresh['travel_mate_id'] = travel_mate.travel_mate_id
        travel_mate_data = TravelMateSerializer(travel_mate, context={'request': request}).data
        tokens_data ={
            'refresh' : str(refresh),
            'access' : str(refresh.access_token)
        }
        data = {
            'tokens_data' : tokens_data,
            'travel_mate_data':travel_mate_data,
        }
        return Response(data)
    
    
class RegisterView(CustomViewHandler,CreateAPIView):
        
    authentication_classes = []
    permission_classes = []
    
    serializer_class = TravelMateSerializer
    queryset = TravelMate.objects.all()
    
    
class Logout(CustomViewHandler,APIView):    
    def post(self, request):
        return Response()


class TravelMateUpdate(CustomViewHandler,UpdateAPIView):
    serializer_class = TravelMateSerializer
    queryset = TravelMate.objects.all()
    lookup_field = 'travel_mate_id'

class OtpSendView(CustomViewHandler,APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        otp = random.randint(100000,999999)
        phone = request.data.get('phone')
        travel_mate = TravelMate.objects.get(phone = phone)
        Otp.objects.create(travel_mate = travel_mate, otp=otp)
        return Response({'detail': "Otp sent!"})

class OtpVerificationView(CustomViewHandler,APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        phone = request.data.get('phone')
        otp = request.data.get('otp')
        travel_mate = TravelMate.objects.get(phone = phone)
        current_time = timezone.now()
        try:
            valid_otps = Otp.objects.filter(travel_mate = travel_mate, expiry_time__gte=current_time)
            valid_otp = valid_otps.order_by('-create_at').first()
            if valid_otp.otp == str(otp) :
                valid_otps.delete()
                return Response({'status' : True, 'msg' : 'Otp verification completed successfully!'})
            else:
                return Response({'status' : False, 'msg' : 'Invalid otp!'})
        except:
            return Response({'status': False, 'msg' : 'Otp expired!'})            

class ForgotPassword(CustomViewHandler,APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        phone = request.data.get('phone')
        new_password = request.data.get('new_password')
        travel_mate = TravelMate.objects.get(phone = phone)
        travel_mate.set_password(new_password)
        travel_mate.save()
        password_change(travel_mate.first_name, travel_mate.email, travel_mate.phone)
        return Response({'detail': 'Passwords updated successfully, Login now!'})

class GetTravelMate(CustomViewHandler,APIView):
    
    def get(self, request, travel_mate_id):
        travel_mate = TravelMate.objects.get(travel_mate_id = travel_mate_id)
        data = TravelMateSerializer(travel_mate, context = {'request': self.request}).data
        return Response(data)

class ResetPassword(CustomViewHandler,APIView):
    
    def post(self, request):
        travel_mate = request.travel_mate
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        TravelMate.objects.change_password(travel_mate, old_password, new_password)
        password_change(travel_mate.first_name, travel_mate.email, travel_mate.phone)        
        return Response({'detail':'Password changed!'})
