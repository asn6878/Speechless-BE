# drf 관련 라이브러리
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets, exceptions, status
from rest_framework.response import Response
from rest_framework.decorators import action

# drf 권한 관련 라이브러리
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

# models.py
from estimate.models import Estimate
from .models import Offer

# serializers.py


class OfferView(APIView):
    # pk값의 견적서 안에있는 입찰제안서 목록 조회
    def get(self, request, pk):
        permission_classes = [AllowAny]
        offers = Offer.objects.all()
        serializer = OfferListSerializer(offers, many=True)
        return Response(serializer.data)
    
    def post(self, request, pk):
        permission_classes = [IsAuthenticated]
