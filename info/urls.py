from django.urls import path, include
from rest_framework.routers import DefaultRouter
from info.views import NoticeViewSet, BannerViewSet

router = DefaultRouter()
router.register(r'notices', NoticeViewSet)
router.register(r'banners', BannerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
