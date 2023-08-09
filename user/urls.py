from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from user.views import NotificationViewSet, ReviewViewSet, MessageViewSet

# simple jwt 관련 모듈
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register('', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/tokens/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refreshments/', TokenRefreshView.as_view(), name='token_refresh'),
]

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'messages', MessageViewSet)


urlpatterns = [
    path('', include(router.urls)),
]

