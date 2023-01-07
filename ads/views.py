from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Ad
from .serializers import AdSerializer
from .permissions import IsPublisherOrReadOnly
from .pagination import StandardResultsSetPagination


class AdListView(APIView, StandardResultsSetPagination):
    permission_classes = [IsPublisherOrReadOnly]
    serializer_class = AdSerializer

    def get(self, request):
        queryset = Ad.objects.filter(is_public=True)
        result = self.paginate_queryset(queryset, request)
        serializer = AdSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)


class AdCreateView(APIView):
    permission_classes = [IsAuthenticated, IsPublisherOrReadOnly]
    serializer_class = AdSerializer
    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = AdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['publisher'] = self.request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class AdDetailView(APIView):
    permission_classes = [IsAuthenticated, IsPublisherOrReadOnly]
    serializer_class = AdSerializer
    parser_classes = [MultiPartParser]

    def get_object(self, pk):
        try:
            return Ad.objects.get(pk=pk)
        except Ad.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        ad = self.get_object(pk)
        serializer = AdSerializer(instance=ad)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        ad = self.get_object(pk)
        serializer = AdSerializer(instance=ad, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        ad = self.get_object(pk)
        ad.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


