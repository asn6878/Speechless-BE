from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from user.views import NotificationViewSet, ReviewViewSet
# simple jwt 관련 모듈
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register('', views.UserViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'reviews', ReviewViewSet)
# router.register(r'messages', MessageViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/tokens/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refreshments/', TokenRefreshView.as_view(), name='token_refresh'),
    path('recover/id/', views.EmailIdFindView.as_view(), name='recover_id'),
    path('recover/password/modifications/', views.EmailPasswdUpdateView.as_view(), name='password_modification'),
    path('auth/', views.UserAuthView.as_view(), name='auth'),
]


