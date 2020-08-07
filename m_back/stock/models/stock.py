from common import *
from django.db import models

class Company(DateModel, BaseActiveModel, BaseNameModel):
    code = models.CharField(
        help_text='회사 종목 코드',
        primary_key=True,
        unique=True,
        max_length=50
    )

class DailyPrice(OHLC):
    models.DateField(
        help_text='날짜별 주식시세',
        auto_now=True,
        primary_key=True
    )
    diff = models.IntegerField(blank=False)
    volume = models.IntegerField(blank=False)    