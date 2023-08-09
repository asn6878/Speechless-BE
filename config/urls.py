from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions

# swagger 관련 모듈
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='Toy_Project_Blog',
        default_version='0.0',
        description='영남대 멋사 11기 말문희막힘팀 해커톤 API 문서입니다.',
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="a@a.com"),     # 부가 정보
        license=openapi.License(name="test")
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('user.urls')),
    path('api/info/', include('info.urls')),
    path('api/estimates' , include('estimate.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name="schema-json"),
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
        ]


