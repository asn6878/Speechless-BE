# drf 관련 라이브러리
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets, exceptions, status
from rest_framework.response import Response
from rest_framework.decorators import action


# drf 권한 관련 라이브러리
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

# models.py
from .models import Estimate
# serializers.py
from .serializers import EstimateDetailSerializer, EstimateListSerializer, EstimateCreateSerializer, OfferListSerializer

class EstimateViewSet(viewsets.ModelViewSet):
    queryset = Estimate.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            print("EstimateViewSet create called")
            return None
        elif self.action == 'retrieve':
            return EstimateDetailSerializer
        elif self.action == 'update' :
            return EstimateDetailSerializer
        elif self.action == 'list' :
            return EstimateListSerializer
        elif self.action == 'destroy' :
            return EstimateListSerializer
        else :
            # 잘못된 요청임을 알리는 예외 발생
            raise exceptions.MethodNotAllowed(self.request.method)

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action == 'retrieve':
            return [AllowAny()]
        elif self.action == 'update' :
            return [IsAuthenticated()]
        elif self.action == 'list' :
            return [AllowAny()]
        elif self.action == 'destroy' :
            return [IsAuthenticated()]
        else:
            return [AllowAny()]
        
    def create(self, request):
        # 여기서 생성되는 Estimate object는, user_info 필드에 request.user.user_id 값이 user_id 인 User object가 들어간다.

        serializer = EstimateCreateSerializer(data={
            'title': request.data.get('title'),
            'user_info': request.user,
            'video': request.data.get('video'),
            'content': request.data.get('content'),
            'dead_line': request.data.get('dead_line'),
            'status': request.data.get('status'),
        })
        if serializer.is_valid():
            self.serializer_class = serializer
            estimate = serializer.save()
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    


    def update(self, request, *args, **kwargs):
        user = request.user
        if request.user != None:
            # jwt토큰 payload에 있는 user_id가 self object의 user_info 필드의 user_id와 같은지 비교.
            if user.user_id == self.get_object().user_info.user_id:
                return super().update(request, *args, **kwargs)
            else :
                raise exceptions.PermissionDenied('수정 권한이 없습니다.')
        else :
            raise exceptions.PermissionDenied('로그인이 필요합니다.')   

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if request.user != None:
            # jwt토큰 payload에 있는 user_id가 self object의 user_info 필드의 user_id와 같은지 비교.
            if user.user_id == self.get_object().user_info.user_id:
                return super().destroy(request, *args, **kwargs)
            else :
                raise exceptions.PermissionDenied('삭제 권한이 없습니다.')
        else :
            raise exceptions.PermissionDenied('로그인이 필요합니다.')
                

# class OfferListView(APIView):
#     # 해당 id 견적글의 Offer List 조회
#     def get(self, request, pk):
#         permission_classes = [AllowAny]
#         offers = Offer.objects.filter(offer_id.estimate_id = pk)
#         serializer = OfferListSerializer(offers, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     # 해당 id 견적글에 입찰하기
#     def post(self, request, pk):
#         permission_classes = [IsAuthenticated]
#         serializer = OfferListSerializer(data=request.data)



#     def offers(self, request, pk):
