from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns = [
   path('login',LoginView.as_view()),
   path('register',RegisterView.as_view()),
   path('travel_mate/<str:travel_mate_id>',GetTravelMate.as_view()),
   path('update/<str:travel_mate_id>',TravelMateUpdate.as_view()),
   path('logout',TokenRefreshView.as_view()),
   path('forgot-password',TokenRefreshView.as_view()),
   path('change-password',ResetPassword.as_view()),
   path('token-refresh',TokenRefreshView.as_view()),
]

