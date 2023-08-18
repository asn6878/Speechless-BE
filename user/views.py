# drf 관련 라이브러리
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework import exceptions
from .models import Notification, Review, Message
from .serializers import NotificationSerializer, ReviewSerializer, MessageSerializer, PasswordChangeSerializer, PasswordChangeReturnSerializer, PasswordMatchSerializer,UserIndexReturnSerializer
from rest_framework import status
from django.http import JsonResponse

# swagger
from drf_yasg.utils import swagger_auto_schema

# drf 권한 관련 라이브러리
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .authentication import JWTAuthentication

# serializers.py
from .serializers import UserSerializer, UserCreateSerializer, UserInfoSerializer
from .serializers import EmailFindSerializer, IdReturnSerializer

# User 모델
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes_by_action = {
        'create': [AllowAny],
        'retrieve': [AllowAny],
        'update': [IsAuthenticated],
        'list': [IsAuthenticated],
        'destroy': [IsAuthenticated],
        'partial_update': [AllowAny],
    }
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
        elif self.action == 'partial_update' :
            return UserCreateSerializer
        else:
            # 잘못된 요청임을 알리는 예외 발생
            raise exceptions.MethodNotAllowed(self.request.method)

    # 각 기능을 커스터마이징(여기서는 비밀번호 암호화) 하기위해 오버라이딩 해줬다.
    def create(self, request, *args, **kwargs):
        print(request.data)
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

    # 부분수정    
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    

# 알림
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

#리뷰
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

#쪽지
# class MessageView(APIView):
#     def post(self, request):
#         # msg_serializer = 
#         pass

class SentMessageView(APIView):
    def get(self, request):
        messages = Message.objects.filter(sender=request.user)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

class ReceivedMessageView(APIView):
    def get(self, request):
        messages = Message.objects.filter(receiver=request.user)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    

class EmailIdFindView(APIView):
    @swagger_auto_schema(request_body=EmailFindSerializer)
    def post(self, request):
        permission_classes = [AllowAny]
        serializer = EmailFindSerializer(data=request.data)
        if serializer.is_valid():
            if User.objects.filter(email = request.data['email']).exists():
                user = User.objects.get(email = request.data['email'])
                response_serializer = IdReturnSerializer(user)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            else :
                return Response({
                    "error" : "해당 이메일로 가입된 아이디가 없습니다."
                }, status = status.HTTP_400_BAD_REQUEST)
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class EmailPasswdUpdateView(APIView):
    @swagger_auto_schema(request_body=PasswordChangeReturnSerializer)
    def post(self, request):
        permission_classes = [AllowAny]
        serializer = PasswordChangeReturnSerializer(data=request.data)
        
        if serializer.is_valid():
            requested_user_id = serializer.data['user_id']
            if User.objects.filter(user_id = requested_user_id).exists():
                user = User.objects.get(user_id = requested_user_id)
                user.set_password(request.data['password'])
                user.save()
                response_serializer = PasswordChangeSerializer(user)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            else :
                return Response({
                    "error" : "해당 user_id의 User가 존재하지 않습니다."
                }, status = status.HTTP_400_BAD_REQUEST)
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordMatchView(APIView):
    @swagger_auto_schema(request_body=PasswordMatchSerializer)
    def post(self, request):
        permission_classes = [AllowAny]
        serializer = PasswordMatchSerializer(data=request.data)
        if serializer.is_valid():
            if User.objects.get(id = serializer.data['id']) == User.objects.get(email = serializer.data['user_email']):
                response_serializer = UserIndexReturnSerializer(User.objects.get(email = serializer.data['user_email']))
                return Response(response_serializer.data,status=status.HTTP_200_OK)
            else :
                return Response(
                    {
                    "detail" : "해당하는 User 존재하지 않음! "
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAuthView(APIView):
    def get(self, request):
        permission_classes = [IsAuthenticated]
        user = request.user
        auth_user = User.objects.get(user_id = user.user_id)
        serializer = UserSerializer(auth_user)
        return Response(serializer.data ,status=status.HTTP_200_OK)    

    
class UserLogoutView(APIView):
    def get(self, request):
        response = Response({
            "message": "Logout success"
            }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie('ACCESS_TOKEN')

        return response
