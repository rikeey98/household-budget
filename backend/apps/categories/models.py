from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Category(models.Model):
    """
    수입/지출 분류 모델
    Self-referencing 구조로 대분류/소분류 지원
    """
    
    CATEGORY_TYPES = [
        ('income', '수입'),
        ('expense', '지출'),
    ]
    
    name = models.CharField(max_length=50, verbose_name='분류명')
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='children',
        verbose_name='상위 분류'
    )
    category_type = models.CharField(
        max_length=10, 
        choices=CATEGORY_TYPES,
        verbose_name='분류 타입'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name='사용자'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    
    class Meta:
        db_table = 'category'
        verbose_name = '분류'
        verbose_name_plural = '분류들'
        # 동일 사용자 내에서 같은 상위분류에 동일한 이름의 분류 중복 방지
        unique_together = ['name', 'parent', 'user']
        indexes = [
            models.Index(fields=['user', 'category_type']),
            models.Index(fields=['parent']),
        ]
    
    def clean(self):
        """모델 유효성 검사"""
        # 부모 분류와 자식 분류의 타입이 같은지 확인
        if self.parent and self.parent.category_type != self.category_type:
            raise ValidationError('상위 분류와 분류 타입이 일치해야 합니다.')
        
        # 자기 자신을 부모로 설정하는 것 방지
        if self.parent and self.parent.id == self.id:
            raise ValidationError('자기 자신을 상위 분류로 설정할 수 없습니다.')
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    @property
    def is_parent(self):
        """대분류 여부"""
        return self.parent is None
    
    @property
    def full_name(self):
        """전체 분류명 (대분류 > 소분류)"""
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name
    
    def __str__(self):
        return self.full_name
