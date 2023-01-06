from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import generics
from .models import Ad
from .serializers import AdSerializer
from .permissions import IsPublisherOrReadOnly
from .pagination import StandardResultsSetPagination


class AdListView(APIView):
    permission_classes = [IsPublisherOrReadOnly]
    serializer_class = AdSerializer
    def get(self, request):
        queryset = Ad.objects.filter(is_public=True)
        serializer = AdSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
