# drf 관련 라이브러리
from rest_framework import viewsets
from django.contrib.auth.hashers import make_password
from rest_framework import exceptions

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
            print("이상한 요청")
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
        self.authentication_classes = []
        instance = request.data.get('password')
        request.data['password'] = make_password(instance)

        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        # 인증
        user = authenticate(request)
        print("views.py authenticate Return 값",user)
        instance = request.data.get('password')
        request.data['password'] = make_password(instance)

        return super().update(request, *args, **kwargs)