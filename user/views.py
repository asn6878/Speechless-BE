# drf 관련 라이브러리
from rest_framework import viewsets
from django.contrib.auth.hashers import make_password
from rest_framework import exceptions
from .models import Notification, Review, Message
from .serializers import NotificationSerializer, ReviewSerializer, MessageSerializer


# drf 권한 관련 라이브러리
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .authentication import JWTAuthentication

# serializers.py
from .serializers import UserSerializer, UserCreateSerializer, UserInfoSerializer


# User 모델
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    # 기능별로 다른 시리얼라이저를 사용
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'retrieve':
            return UserInfoSerializer
        elif self.action == 'update' :
            return UserCreateSerializer 
        elif self.action == 'list' :
            return UserInfoSerializer
        elif self.action == 'destroy' :
            return UserSerializer
        else:
            # 잘못된 요청임을 알리는 예외 발생
            raise exceptions.MethodNotAllowed(self.request.method)

    # 기능별로 다른 권한을 사용 
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        elif self.action == 'retrieve':
            return [AllowAny()]
        elif self.action == 'update' :
            return [IsAuthenticated()]
        elif self.action == 'list' :
            return [IsAuthenticated()]
        elif self.action == 'destroy' :
            return [IsAuthenticated()]
        else:
            return [AllowAny()]

    # 각 기능을 커스터마이징(여기서는 비밀번호 암호화) 하기위해 오버라이딩 해줬다.
    def create(self, request, *args, **kwargs):
        instance = request.data.get('password')
        request.data['password'] = make_password(instance)

        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        # 인증
        user = request.user
        if request.user != None:
            # jwt토큰 payload에 있는 user_id가 url에 들어온 pk와 같은지 비교.
            if user.user_id == int(kwargs['pk']):

                instance = request.data.get('password')
                request.data['password'] = make_password(instance)

                return super().update(request, *args, **kwargs)
            else:
                raise exceptions.PermissionDenied('수정 권한이 없습니다.')
        else:
            # 현재 토큰이 존재하지 않음.
            raise exceptions.AuthenticationFailed('로그인이 필요합니다.')
        
    def destroy(self, request, *args, **kwargs):
        user = request.user
        if request.user != None:
            # jwt토큰 payload에 있는 user_id가 url에 들어온 pk와 같은지 비교.
            if user.user_id == int(kwargs['pk']):
                return super().destroy(request, *args, **kwargs)
            else :
                raise exceptions.PermissionDenied('삭제 권한이 없습니다.')
        else :
            raise exceptions.PermissionDenied('로그인이 필요합니다.')
# 알림
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

#리뷰
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

#쪽지
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
