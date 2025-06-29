from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

class UserIsolationMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # 인증이 필요한 API만 필터링 (예: /api/로 시작)
        if request.path.startswith('/api/'):
            if not request.user.is_authenticated:
                return JsonResponse({'detail': '인증이 필요합니다.'}, status=401)
            # 추가로, 필요하다면 request에 사용자 정보 주입 등 가능
        return None
