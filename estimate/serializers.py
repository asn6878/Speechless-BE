from rest_framework import serializers
from .models import Estimate
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'user_id',
            'user_name',
        ]


# 견적 리스트 시리얼라이저
class EstimateListSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(read_only = True)

    class Meta:
        model = Estimate
        fields = [
            'estimate_id',
            'estimate_title',
            'user_info',
            'created_at',
        ]


class EstimateDetailSerializer(serializers.ModelSerializer):
    