from django.db import models
from django.conf import settings
from decimal import Decimal


class AssetSnapshot(models.Model):
    """
    자산 스냅샷 모델
    정기적인 자산 현황 기록
    """
    
    ASSET_TYPES = [
        ('cash', '현금/예금'),
        ('stock', '주식'),
        ('real_estate', '부동산'),
        ('loan', '대출'),
        ('pension', '연금'),
        ('other', '기타'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='asset_snapshots',
        verbose_name='사용자'
    )
    asset_type = models.CharField(
        max_length=20,
        choices=ASSET_TYPES,
        verbose_name='자산 유형'
    )
    asset_name = models.CharField(
        max_length=100,
        verbose_name='자산명'
    )
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=0,  # 원 단위만 관리
        verbose_name='평가금액',
        help_text='부채는 음수로 입력'
    )
    snapshot_date = models.DateField(verbose_name='기록날짜')
    memo = models.TextField(
        blank=True,
        verbose_name='메모'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    
    class Meta:
        db_table = 'asset_snapshot'
        verbose_name = '자산 스냅샷'
        verbose_name_plural = '자산 스냅샷들'
        # 동일 사용자의 같은 자산에 대해 같은 날짜 중복 방지
        unique_together = ['user', 'asset_type', 'asset_name', 'snapshot_date']
        indexes = [
            models.Index(fields=['user', 'snapshot_date']),
            models.Index(fields=['user', 'asset_type']),
        ]
        ordering = ['-snapshot_date', 'asset_type', 'asset_name']
    
    @property
    def formatted_amount(self):
        """금액을 천단위 콤마로 포맷"""
        if self.amount >= 0:
            return f"{self.amount:,}원"
        else:
            return f"-{abs(self.amount):,}원"
    
    @property
    def is_debt(self):
        """부채 여부 (음수 금액)"""
        return self.amount < 0
    
    def __str__(self):
        return f"{self.snapshot_date} - {self.asset_name}: {self.formatted_amount}"
