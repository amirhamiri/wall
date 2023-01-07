from rest_framework import serializers
from .models import Ad


class AdSerializer(serializers.ModelSerializer):
    publisher = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Ad
        fields = '__all__'
        read_only_fields = ('id', 'date_added', 'is_public')
        extra_kwargs = {'image': {'required': False}}
