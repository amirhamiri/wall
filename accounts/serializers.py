from django.contrib.auth import authenticate, password_validation
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'password', 'username')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_password(self, value):
        try:
            password_validation.validate_password(value, self.instance)
        except serializers.ValidationError as error:
            self.add_error('password', error)
        return value


class GetOtpSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=4)

    def save(self, validated_data):
        refresh = RefreshToken.for_user(validated_data)
        return ({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
