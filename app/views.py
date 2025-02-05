from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from app.models import *
from app.GPTRequests import *
from .serializer import *
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
import json
import threading # threading.Thread(target=background_task).start()
import requests
import os


# LinkedIn credentials from settings.py
CLIENT_ID = os.environ.get('LINKEDIN_CLIENT_ID')
CLIENT_SECRET = os.environ.get('LINKEDIN_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('LINKEDIN_REDIRECT_URI')

# Create your views here.
@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username = request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    token , created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    user = serializer.data
    user["password"] = "password"
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
        u = serializer.data
        u["password"] = "password"
        return Response({"token": token.key, "user": u})
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


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        # Extract email parameters from request body
        subject = data.get('subject')
        message = data.get('message')
        from_email = data.get('from_email')
        recipient_list = data.get('recipient_list')
        cc = data.get('cc', [])
        bcc = data.get('bcc', [])

        html_content = render_to_string(
            data.get('templateName', '') + ".html",
            data.get('content'))

        # Create EmailMessage object with HTML content
        email = EmailMessage(subject, html_content, from_email, recipient_list, cc, bcc)
        email.content_subtype = 'html'  # Set the content type to HTML

        try:
            email.send()
            return JsonResponse({'Message': 'Email sent successfully.', "Status":200, "Payload":{}}, status=200)
        except Exception as e:
            return JsonResponse({'error': '{}'.format(e)}, status=400)
    return JsonResponse({'message': 'Method Not Allowed', "Status": 415, "Payload":{}}, status=415)



@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def saveFieldsToQuery(request):
    user = request.user
    if serializer.is_valid():
        serializer.save(user=user)  # Associate the user with the Profile record
        return Response({"post": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
class FieldsToQueryAPIView(APIView):
    def fieldsToQuery(self, request):
        queryset = FieldsToQuery.objects.all()

        # Filter queryset based on query parameters
        for key, value in request.data.items():
            kwargs = {f'{key}__icontains': value}  # Case-insensitive partial match
            queryset = queryset.filter(**kwargs)

        serializer = FieldsToQuerySerializer(queryset, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def createQueryToGetFields(request):
    user = request.user
    serializer = FieldsToQuerySerializer(data=request.data)
    if serializer.is_valid():
        fieldObj = serializer.validated_data
        serializer.save(user=user)
        res = json.loads(GPTRequests.getTopicsToWriteOn(fieldObj["title"]))
        for title in res.get("titles", []):
            print(title.get("title"))
            reseacrhpapers = ResearchPapers(
                prompt=title.get("title"),
                response=str(res),
                socialMedia=fieldObj["socialMedia"],
                user=user
            )
            reseacrhpapers.save()

            post = Posts(
                rPaper = reseacrhpapers,
                user = user,
                topic = title.get("title"),
                socialsName =fieldObj["socialMedia"],
                content = "",
                posted = False,
                approved = False,
                reviewed = False
            )
            post.save()
        return Response(res)
    return Response({"error" : serializer.errors})

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def createArticle(request):
    user = request.user
    data = json.loads(request.body)
    try:
        # Try to get the existing ResearchPapers record for the authenticated user
        rPaper = ResearchPapers.objects.get(pk=data.get("id"))
        serializer = ResearchPapersSerializer(rPaper, data=rPaper.__dict__)
        createArticles(rPaper, name="rPaper")
        return Response({"status" : "success"})
    except ResearchPapers.DoesNotExist:
        return Response({"error" : "Research Paper Not found"})


def createArticles(param, **kwargs):
    print("createArticles -> ()")
    for key, value in kwargs.items():
        if key == "name" and value == "id":
            rPaper = ResearchPapers.objects.get(pk=param)
        elif key == "name" and value == "rPaper":
            rPaper = param
    posts = rPaper.posts.all()
    for post in posts:
        makeRequestForArtciles(post)

def makeRequestForArtciles(post):
    print("makeRequestForArtciles -> ()")
    res = GPTRequests.getArticlesToPost(post.topic)
    post.content = res
    post.save()

def crunchResponseFromArticlesApiCall(post, response):
    print()
    pass


def linkedinCallback(request):
    print("Got called ---> ")
    code = request.GET.get('code')
    state = request.GET.get('state')
    print(code)

    if not code:
        return JsonResponse({'error': 'Authorization code not found'}, status=400)

    # Step 3: Exchange Authorization Code for Access Token
    token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    response = requests.post(token_url, data=payload)
    if response.status_code != 200:
        return JsonResponse({'error': 'Failed to get access token', 'details': response.json()}, status=400)

    access_token = response.json().get('access_token')
    expires_in = response.json().get('expires_in')

    return JsonResponse({
        'access_token': access_token,
        'expires_in': expires_in
    })