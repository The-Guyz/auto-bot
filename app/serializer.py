from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'email', 'username', 'password']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Profile
        fields = ['firstName', 'middleName', 'email', 
            'companyRole', 'lastName', 'country', 'phoneNumber']

class CompanySerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Company
        fields = ['name', 'email', 'energyOperationCertificate', 'accNumber', 'bankName']


class PostsSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Posts
        fields = ['topic', 'socialsName', 'content', 'posted', 'approved', 'reviewed']

class ResearchPapersSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = ResearchPapers
        fields = ['prompt', 'response']


