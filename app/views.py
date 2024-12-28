from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from app.models import *
from .serializer import *
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
# Create your views here.   

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username = request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    token , created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    user = serializer.data
    return Response({"token": token.key, "user": user})

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        profile = Profile()
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed for {}".format(request.user.email))


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def saveProfile(request):
    user = request.user
    try:
        # Try to get the existing Profile record for the authenticated user
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile, data=request.data)
    except Profile.DoesNotExist:
        # If no Profile record exists, create a new one
        serializer = ProfileSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=user)  # Associate the user with the Profile record
        return Response({"profile": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class ProfileListAPIView(APIView):
    def post(self, request):
        queryset = Profile.objects.all()

        # Filter queryset based on query parameters
        for key, value in request.data.items():
            kwargs = {f'{key}__icontains': value}  # Case-insensitive partial match
            queryset = queryset.filter(**kwargs)

        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def saveCompany(request):
    user = request.user
    try:
        # Try to get the existing Profile record for the authenticated user
        company = Company.objects.get(user=user)
        serializer = CompanySerializer(company, data=request.data)
    except Company.DoesNotExist:
        # If no Profile record exists, create a new one
        serializer = CompanySerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=user)  # Associate the user with the Profile record
        return Response({"company": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class CompanyListAPIView(APIView):
    def post(self, request):
        queryset = Company.objects.all()

        # Filter queryset based on query parameters
        for key, value in request.data.items():
            kwargs = {f'{key}__icontains': value}  # Case-insensitive partial match
            queryset = queryset.filter(**kwargs)

        serializer = CompanySerializer(queryset, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def savePost(request):
    user = request.user
    try:
        # Try to get the existing Profile record for the authenticated user
        post = get_object_or_404(Posts, user=user, topic=request.data['topic'])
        serializer = PostsSerializer(post, data=request.data)
    except Posts.DoesNotExist:
        # If no Profile record exists, create a new one
        serializer = PostsSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=user)  # Associate the user with the Profile record
        return Response({"post": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class PostsAPIView(APIView):
    def post(self, request):
        queryset = Posts.objects.all()

        # Filter queryset based on query parameters
        for key, value in request.data.items():
            kwargs = {f'{key}__icontains': value}  # Case-insensitive partial match
            queryset = queryset.filter(**kwargs)

        serializer = PostsSerializer(queryset, many=True)
        return Response(serializer.data)