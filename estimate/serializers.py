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
    user_info = UserSerializer(source='user_id', read_only = True)

    class Meta:
        model = Estimate
        fields = [
            'estimate_id',
            'title',
            'user_info',
            'created_at',
        ]

# 견적 상세 시리얼라이저
class EstimateDetailSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(read_only = True)

    class Meta:
        model = Estimate
        fields = [
            'user_info',
            'title',
            'created_at',
            'video',
            'content',
            'dead_line',
            'status',
        ]
 
# 견적 생성 시리얼라이저
class EstimateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estimate
        fields = [
            'title',
            'created_at',
            'video',
            'content',
            'dead_line',
            'status',
        ]

    def create(self, validated_data):
        # 인증된 user 값 받기
        user = self.context['request'].user
        if user.is_anonymous:
            raise serializers.ValidationError('로그인이 필요합니다.')
        # print("호출된 유저 id",user.user_id)
        # estimate 오브젝트 생성 (user_id 필드에는 user 오브젝트 넣어준다.)
        estimate = Estimate.objects.create(user_id=user, **validated_data)
        return estimate


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