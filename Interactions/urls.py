from django.urls import path
from Interactions.Trips.Likes.views import CreateTripLike , GetTripLikesView
from Interactions.Trips.Comments.views import CreateTripComment, GetTripCommentsView, CreateReplyToTripComment
from Interactions.Trips.Requests.views import (CreateTripRequest, DeleteRequest,
    GetTripRequestsView, TripRequestAcceptView)
from Interactions.Trips.Follow.views import FollowView,GetTravelMateFollowers,GetTravelMateFollowings
from Interactions.views import InteractionsView

urlpatterns = [
    # Trips-likes
    path('trips/likes/like',CreateTripLike.as_view()),
    path('trips/likes/get-likes/<str:trip_id>',GetTripLikesView.as_view()),
    
    # Trips-comments
    path('trips/comments/comment',CreateTripComment.as_view()),
    path('trips/comments/get-comments/<str:trip_id>',GetTripCommentsView.as_view()),
    path('trips/comments/reply/<str:comment_id>',CreateReplyToTripComment.as_view()),
    
    # Trips-requests
    path('trips/requests/request',CreateTripRequest.as_view()),
    path('trips/requests/get-requests/<str:trip_id>',GetTripRequestsView.as_view()),
    path('trips/requests/delete-request/<str:request_id>',DeleteRequest.as_view()),
    path('trips/requests/accept/<str:request_id>',TripRequestAcceptView.as_view()),
    
    # Followings
    path('followings/follow/<str:travel_mate_id>',FollowView.as_view()),
    path('followings/get-followers/<str:travel_mate_id>',GetTravelMateFollowers.as_view()),
    path('followings/get-followings/<str:travel_mate_id>',GetTravelMateFollowings.as_view()),
    
    # Interactions
    path('interactions',InteractionsView.as_view()),
    ]