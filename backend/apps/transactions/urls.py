from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, WeeklySummaryAPIView

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
    path('weekly-summary/', WeeklySummaryAPIView.as_view(), name='transactions-weekly-summary'),
]