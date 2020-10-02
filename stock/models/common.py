from django.db import models
from django.utils import timezone
# Create your models here.
class DateModel(models.Model):
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=False,
        verbose_name="생성 일시",
        help_text="데이터가 생성된 날짜입니다.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        blank=True,
        null=False,
        verbose_name="수정 일시",
        help_text="데이터가 수정된 날짜입니다.",
    )

    class Meta:
        abstract = True


class BaseActiveModel(models.Model):
    
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="활성화 여부",
        help_text="활성화할지 여부를 결정합니다.",
    )

    class Meta:
        abstract = True


class BaseNameModel(models.Model):
    name_en = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        verbose_name="영어 명칭",
        help_text="고유 영어 명칭을 나타냅니다.",
    )
    name_ko = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        verbose_name="한국어 명칭",
        help_text="고유 한국어 명칭을 나타냅니다.",
    )

    class Meta:
        abstract = True


class UserMixin(models.Model):
    
    user_id = models.UUIDField(
        null=False,
        blank=False,
        verbose_name="유저",
        help_text="어느 유저의 정보인지 나타냅니다.",
    )

    class Meta:
        abstract = True

class OHLC(models.Model):
    # Open-high-low-close chart
    open_price = models.IntegerField(blank=False)
    high_price = models.IntegerField(blank=False)
    low_price = models.IntegerField(blank=False)
    close_price = models.IntegerField(blank=False)

    class Meta:
        abstract = True