from django.urls import path

from .views import (
    RegisterView, 
    MyTokenObtainPairView, 
    TweetListCreateView, 
    FollowUnfollowView, 
    FeedView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('tweets/', TweetListCreateView.as_view(), name='tweets'),
    path('follow/<int:pk>/', FollowUnfollowView.as_view(), name='follow_unfollow'),
    path('feed/', FeedView.as_view(), name='feed'),
]