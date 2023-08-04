# drf 관련 라이브러리
from rest_framework import viewsets
from django.contrib.auth.hashers import make_password

# drf 권한 관련 라이브러리
from rest_framework.permissions import IsAuthenticated, AllowAny

# serializers.py
from .serializers import UserSerializer, UserCreateSerializer, UserInfoSerializer

# models.py
from .models import CustomUser

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()

    # 기능별로 다른 시리얼라이저를 사용!
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
            print("5개의 기능중 그 무엇도 아닌 이상한 요청이 들어옴.")
            print(self.action)
            return UserSerializer

    # 각 기능을 커스터마이징 하기위해 오버라이딩 해줬다.
    def create(self, request, *args, **kwargs):
        permission_classes = [AllowAny]
        instance = request.data.get('password')
        request.data['password'] = make_password(instance)

        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        permission_classes = [IsAuthenticated]

        instance = request.data.get('password')
        request.data['password'] = make_password(instance)

        return super().update(request, *args, **kwargs)
    
