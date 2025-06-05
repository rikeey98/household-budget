from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal


class Transaction(models.Model):
    """
    수입/지출 거래 모델
    """
    
    TRANSACTION_TYPES = [
        ('income', '수입'),
        ('expense', '지출'),
    ]
    
    PAYMENT_METHODS = [
        ('cash', '현금'),
        ('card', '카드'),
        ('account', '계좌이체'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name='사용자'
    )
    date = models.DateField(verbose_name='거래일')
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=0,  # 원 단위만 관리
        verbose_name='금액'
    )
    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPES,
        verbose_name='거래 타입'
    )
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.PROTECT,  # 분류 삭제 시 거래는 보호
        related_name='transactions',
        verbose_name='분류'
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='설명'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        verbose_name='결제수단'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    
    class Meta:
        db_table = 'transaction'
        verbose_name = '거래'
        verbose_name_plural = '거래들'
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['user', 'transaction_type']),
            models.Index(fields=['category']),
        ]
        ordering = ['-date', '-created_at']
    
    def clean(self):
        """모델 유효성 검사"""
        # 거래 타입과 분류 타입 일치 확인
        if self.category and self.category.category_type != self.transaction_type:
            raise ValidationError('거래 타입과 분류 타입이 일치해야 합니다.')
        
        # 금액은 양수만 허용
        if self.amount <= 0:
            raise ValidationError('금액은 0보다 커야 합니다.')
        
        # 미래 날짜 제한 (선택사항)
        if self.date > timezone.now().date():
            raise ValidationError('미래 날짜는 입력할 수 없습니다.')
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    @property
    def formatted_amount(self):
        """금액을 천단위 콤마로 포맷"""
        return f"{self.amount:,}원"
    
    def __str__(self):
        return f"{self.date} - {self.category.name}: {self.formatted_amount}"
