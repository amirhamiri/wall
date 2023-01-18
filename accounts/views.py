from django.core.cache import cache
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts import serializers
from accounts.otp_service import OTP
from accounts.serializers import UserSerializer

from .models import User
from .permissions import IsUser


class UserView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = UserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = serializers.UserRegisterSerializer(data=request.data)
        otp_service = OTP()
        if serializer.is_valid():
            clean_data = serializer.validated_data
            randcode = otp_service.generate_otp(clean_data['phone'])
           
            cache.set(key='register', value={'phone': clean_data['phone'], 'password': clean_data['password'], 'username': clean_data['username']}, timeout=300)

            return Response({'phone': clean_data['phone'], 'result': 'otp sended'}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class CheckOtpCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = cache.get(key='register')
        serializer = serializers.GetOtpSerializer(data=request.data)
        otp_obj = OTP()
        if data is None:
            return Response({'error': 'this code not exist or invalid'}, status=status.HTTP_404_NOT_FOUND)
        if serializer.is_valid():
            clean_data = serializer.validated_data
            if otp_obj.verify_otp(otp=clean_data['code'], phone=data['phone']):
                user = User.objects.create_user(
                    phone=data['phone'], username=data['username'], password=data['password'])

                result = serializer.save(validated_data=user)
                return Response(result, status=status.HTTP_201_CREATED)
            return Response({'error': 'this code not exist or invalid'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)