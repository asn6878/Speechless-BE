from django.urls import path, include
# s
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('', views.EstimateViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path()
]