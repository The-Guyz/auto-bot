from django.urls import re_path
from app import views
from .views import *

urlpatterns = [
    re_path('login', views.login),
    re_path('signup', views.signup),
    re_path('test_token', views.test_token),
    re_path('saveProfile', views.saveProfile),
    re_path('profiles/', ProfileListAPIView.as_view(), name='profile-list'),
    re_path('saveCompany', views.saveCompany),
    re_path('companies/', CompanyListAPIView.as_view(), name='companies-list'),
    re_path('savePost', views.savePost),
    re_path('posts/', PostsAPIView.as_view(), name='posts-list'),
]