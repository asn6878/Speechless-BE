from django.conf import settings
from django.contrib.auth import get_user_model

# drf 인증, 권한 관련 모듈
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, CSRFCheck

# JWT
import jwt


# 현재 장고 Authentication 에 쓰고있는 User모델을 가져온다.
User = get_user_model()

# settings.py 에 설정된 JWT Authentication 과 관련된 클래스를 작성해준다.
class JWTAuthentication(BaseAuthentication):
    # JWT 토큰을 뜯어내서 헤더에 있는 유저 정보(user_name)를 얻어내는 함수
    def authenticate(self, request):
        jwt_header = request.headers.get('Authorization')

        if not jwt_header:
            return None
        
        try :
            prefix = jwt_header.split(' ')[0]
            if prefix.lower() != 'jwt':
                raise exceptions.AuthenticationFailed('현재 토큰이 jwt 형식이 아닙니다.')
            
            access_token = jwt_header.split(' ')[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256']
            )
        except jwt.ExpiredSignatureError:
            # access 토큰이 만료되었을 때 로직 (refresh 토큰 사용해서 api 요청 보내서 acess 토큰 재발급 받고, 재발급 받은 토큰으로 api 요청 다시 보내는 부분)
            pass
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')
        
        return self.authenticate_credentials(request, payload)
    
    # JWT 토큰을 통해 얻어낸 유저 정보를 활용해 user 객체를 리턴해주는 함수.
    def authenticate_credentials(self, request, key):
        token_user = User.objects.filter(user_id=key).first()

        if token_user is None:
            raise exceptions.AuthenticationFailed('해당하는 User가 존재하지 않습니다.')
        
        self.enforce_csrf(request)
        return (token_user, None)
    
    # CSRF 토큰 검증
    def enforce_csrf(self, request):
        check = CSRFCheck()

        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)

        

