from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

class UserIsolationMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # 인증 예외 엔드포인트 목록
        EXEMPT_PATHS = [
            '/api/accounts/auth/csrf/',
            '/api/accounts/auth/login/',
            '/api/accounts/auth/register/',  # 회원가입도 예외 필요시 추가
        ]
        if request.path in EXEMPT_PATHS:
            return None
        if request.path.startswith('/api/'):
            if not request.user.is_authenticated:
                return JsonResponse({'detail': '인증이 필요합니다.'}, status=401)
            # 추가로, 필요하다면 request에 사용자 정보 주입 등 가능
        return None
