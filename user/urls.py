from django.urls import path, include
# s
from rest_framework.routers import DefaultRouter

from . import views

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

