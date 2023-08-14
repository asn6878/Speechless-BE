# drf 관련 라이브러리
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets, exceptions, status
from rest_framework.response import Response

# swagger
from drf_yasg.utils import swagger_auto_schema
from .swaggers import OfferCreateRequestSerializer

# drf 권한 관련 라이브러리
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

# 모델 관련 라이브러리
from estimate.models import Estimate
from .models import Offer
from django.contrib.auth import get_user_model

# serializers.py
from .serializers import OfferDetailSerializer, OfferCreateSerializer

User = get_user_model()

class OfferView(APIView):

    # pk값의 견적서 안에있는 입찰제안서 목록 조회
#    @swagger_auto_schema(request_body=OfferDetailSerializer)
    def get(self, request, pk):
        permission_classes = [AllowAny]
        offers = Offer.objects.filter(estimate_id = pk)
        serializer = OfferDetailSerializer(offers, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(request_body=OfferCreateRequestSerializer)
    def post(self, request, pk):
        serializer = OfferCreateSerializer(data=request.data)
        try:
            estimate = Estimate.objects.get(estimate_id=pk)
        except Estimate.DoesNotExist:
            raise exceptions.NotFound('해당 id의 견적이 존재하지 않습니다.')

        
        if serializer.is_valid():
            if request.user.is_anonymous:
                raise exceptions.AuthenticationFailed('로그인이 필요합니다.')
            serializer.save(estimate_id=estimate ,user_id=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request, pk):
    #     offer = Offer.objects.get()
    #     serializer = OfferDetailSerializer(offer, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(estimate_id=pk)
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        offer = Offer.objects.get(offer_id = pk)
        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)