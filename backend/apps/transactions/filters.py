# backend/apps/transactions/filters.py
from django_filters import rest_framework as filters
from .models import Transaction

class TransactionFilter(filters.FilterSet):
    # 날짜 범위
    start_date = filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='date', lookup_expr='lte')
    # 금액 범위
    min_amount = filters.NumberFilter(field_name='amount', lookup_expr='gte')
    max_amount = filters.NumberFilter(field_name='amount', lookup_expr='lte')
    # 설명(검색)
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = Transaction
        fields = [
            'transaction_type',   # exact match
            'payment_method',     # exact match
            'category',           # exact match (id)
            # 아래는 커스텀 필터로 처리
            # 'date', 'amount', 'description'
        ]