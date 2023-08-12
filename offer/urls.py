from django.urls import path, include
from .views import *


urlpatterns = [
    path('<int:pk>/', OfferView.as_view(), name='offer_list'),
]