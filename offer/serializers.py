from rest_framework import serializers

# 모델 관련 라이브러리
from estimate.models import Estimate
from django.contrib.auth import get_user_model
from .models import Offer

User = get_user_model()

class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = [
            'offer_id',
            'user_id',
            'title',
            'video',
            'content',
            'price',
            'created_at',
            'status',
        ]
