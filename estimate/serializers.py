from rest_framework import serializers
from .models import Estimate
from django.contrib.auth import get_user_model

User = get_user_model()

# 유저 정보 시리얼라이저
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id',
            'user_name',
            'level',
        ]

# 견적 정보 시리얼라이저
class EstimateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estimate
        fields = ['estimate_id']


# 견적 리스트 시리얼라이저
class EstimateListSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(read_only = True)

    class Meta:
        model = Estimate
        fields = [
            'estimate_id',
            'title',
            'user_info',
            'created_at',
        ]

    def __str__(self):
        return f'estimate_id = {self.estimate_id}'


# 견적 상세 시리얼라이저
class EstimateDetailSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(read_only = True)

    class Meta:
        model = Estimate
        fields = [
            'title',
            'user_info',
            'created_at',
            'video',
            'content',
            'dead_line',
            'status',
        ]

    def __str__(self):
        return f'estimate_id = {self.estimate_id}'
    
# 견적 생성 시리얼라이저
class EstimateCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Estimate
        fields = [
            'title',
            'user_id',
            'created_at',
            'video',
            'content',
            'dead_line',
            'status',
        ]

    def __str__(self):
        return f'estimate_id = {self.estimate_id}'

# 입찰 리스트 시리얼라이저
class OfferListSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(read_only = True)
    estimate_info = EstimateSerializer(read_only = True)

    class Meta:
        model = Estimate
        fields = [
            'offer_id',
            'estimate_info',
            'user_info',
            'price',
            'content',
            'status',
        ]

    def __str__(self):
        return f'offer_id = {self.offer_id}'


    