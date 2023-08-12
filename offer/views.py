# drf 관련 라이브러리
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets, exceptions, status
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes

# drf 권한 관련 라이브러리
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

# models.py
from estimate.models import Estimate
from .models import Offer

# serializers.py
from .serializers import OfferDetailSerializer

class OfferView(APIView):
    permission_classes = [IsAuthenticated]
    # pk값의 견적서 안에있는 입찰제안서 목록 조회
    def get(self, request, pk):
        permission_classes = [AllowAny]
        offers = Offer.objects.filter(estimate_id = pk)
        serializer = OfferDetailSerializer(offers, many=True)
        return Response(serializer.data)
    
    def post(self, request, pk):
        serializer = OfferDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(estimate_id=pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        offer = Offer.objects.get()
        serializer = OfferDetailSerializer(offer, data=request.data)
        if serializer.is_valid():
            serializer.save(estimate_id=pk)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        offer = Offer.objects.get(id = pk)
        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)