from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='login'),
    path('register', views.UserRegisterView.as_view(), name='register'),
    path('check', views.CheckOtpCodeView.as_view(), name='check-otp'),
    path('profile', views.UserView.as_view(),name='profile_view'),
]