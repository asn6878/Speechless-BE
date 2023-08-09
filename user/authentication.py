# django auth 상속 라이브러리
from rest_framework.authentication import BaseAuthentication, CSRFCheck
from django.contrib.auth import get_user_model
from rest_framework import authentication

# jwt decoding 라이브러리
import jwt

# django 관련 라이브러리
from rest_framework import exceptions
from django.conf import settings

User = get_user_model()

# JWTAuthentication 클래스 오버라이딩
class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        jwt_header = request.headers.get('Authorization')
        if not jwt_header:
            return None

        try:
            prefix, token = jwt_header.split(' ')
            if prefix.lower() != 'bearer':
                raise exceptions.AuthenticationFailed('Invalid token prefix')
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            payload_user_id = payload.get('user_id')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')
        except Exception:
            raise exceptions.AuthenticationFailed('Authentication failed')

        return self.authenticate_credentials(request, payload_user_id)

    def authenticate_credentials(self, request, payload_user_id):
        try:
            user = User.objects.get(user_id=payload_user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found')

        # self.enforce_csrf(request)
        return user, None

    # # CSRF 토큰 검증
    # def enforce_csrf(self, request):
    #     check = CSRFCheck()

    #     check.process_request(request)
    #     reason = check.process_view(request, None, (), {})
    #     if reason:
    #         raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)