from rest_framework import serializers
from .models import CustomUser, Notification, Review, Message


# 기본 시리얼라이저
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

# 마이페이지 전용 유저 정보 조회 시리얼라이저 (RETIEVE)
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'user_id',
            'user_name',
            'email',
            'id',
            'prof_img',
            'prof_intro',
            'exp',
            'level',
        ]

# 회원가입 시리얼라이저 (POST)
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'user_name',
            'email',
            'id',
            'password',
        ]
        # 비밀번호 필드를 읽기전용 필드로 설정해두면, response 되는 데이터에서 password 데이터는 오지 않게 됨.
        extra_kwargs = {
            'password': {'write_only': True},
        }

#알림
class NotificationSerializer(serializers.Serializer):
    class Meta:
        model = Notification
        fields = ['notice_id', 'user_id', 'title', 'content', 'is_checked']

#리뷰
class ReviewSerializer(serializers.Serializer):
    class Meta:
        model = Review
        fields = ['review_id', 'user_id', 'content', 'img']
    
#쪽지
class MessageSerializer(serializers.Serializer):
    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'content', 'sent_time']

class EmailFindSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordMatchSerializer(serializers.Serializer):
    user_email = serializers.EmailField()
    id = serializers.CharField()

class IdReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
        ]

class UserIndexReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'user_id',
        ]

class PasswordChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'user_id',
            'password',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

class PasswordChangeReturnSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    password = serializers.CharField()