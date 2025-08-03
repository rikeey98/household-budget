from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import TransactionSerializer
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TransactionFilter
from rest_framework.views import APIView
from .serializers import WeekSummarySerializer, WeeklySummaryResponseSerializer
from datetime import date, timedelta
from django.db.models import Sum, Q
from apps.categories.models import Category
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .services import get_weekly_summary
from rest_framework.generics import GenericAPIView

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter

    def get_queryset(self):
        # 본인 거래만 조회
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        print("==== [트랜잭션 생성 요청] ====")
        print("요청 데이터:", request.data)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("유효성 검사 에러:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        print("생성 성공:", serializer.data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class WeeklySummaryAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WeeklySummaryResponseSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('year', openapi.IN_QUERY, description="년도(예: 2024)", type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('month', openapi.IN_QUERY, description="월(예: 6)", type=openapi.TYPE_INTEGER, required=True),
        ],
        responses={
            200: WeeklySummaryResponseSerializer
        }
    )
    def get(self, request):
        user = request.user
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        if not year or not month:
            return Response({'detail': 'year와 month는 필수입니다.'}, status=400)
        year = int(year)
        month = int(month)
        week_summaries = get_weekly_summary(user, year, month)
        serializer = self.get_serializer({'weeks': week_summaries})
        return Response(serializer.data)
