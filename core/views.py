from django.shortcuts import render

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, Tweet
from .serializers import UserSerializer, TweetSerializer, MyTokenObtainPairSerializer
from .permissions import IsTweetCreatorOrReadOnly

# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class TweetListCreateView(generics.ListCreateAPIView):
    queryset = Tweet.objects.all().order_by('-created_at') 
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FollowUnfollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        print(f"Request received to follow/unfollow user with id {pk}")
        user_to_follow = get_object_or_404(User, pk=pk)
        current_user = request.user

        if user_to_follow in current_user.following.all():
            current_user.following.remove(user_to_follow)
            print(f"User {current_user.id} unfollowed user {user_to_follow.id}")
        else:
            current_user.following.add(user_to_follow)
            print(f"User {current_user.id} followed user {user_to_follow.id}")

        return Response({'status': 'ok'})
    
class FeedView(generics.ListAPIView):
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        return Tweet.objects.filter(user__in=following_users)
    
class UserTweetListView(generics.ListAPIView):
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        return Tweet.objects.filter(user=user).order_by('-created_at')
