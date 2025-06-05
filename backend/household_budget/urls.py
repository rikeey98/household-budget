# household_budget/urls.py
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.http import JsonResponse

def test_api(request):
    return JsonResponse({"message": "CORS 설정이 성공했습니다!", "status": "success"})

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API URLs
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/categories/', include('apps.categories.urls')),
    path('api/transactions/', include('apps.transactions.urls')),
    path('api/assets/', include('apps.assets.urls')),
    
    # API 문서
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/test/', test_api, name='test-api'),  # 테스트용 API
]