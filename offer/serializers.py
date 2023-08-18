from rest_framework import serializers

# 모델 관련 라이브러리
from estimate.models import Estimate
from django.contrib.auth import get_user_model
from .models import Offer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id',
            'level',
            'user_name',
        ]

class OfferDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, source='user_id')
    class Meta:
        model = Offer
        fields = [
            'offer_id',
            'user',
            'content',
            'price',
            'status',
        ]
    
class OfferCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = [
            'content',
            'price',
        ]
