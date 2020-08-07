from .common import *
from django.db import models
from django.utils import timezone
# 반드시 CharField 에는 max_length 를 넣어 줘야 한다.

class Company(DateModel, BaseActiveModel, BaseNameModel):
    code = models.CharField(
        help_text='회사 종목 코드',
        primary_key=True,
        unique=True,
        max_length=50
    )

class DailyPrice(OHLC):    
    date = models.CharField(
        help_text='날짜별 주식시세',
        primary_key=True,
        unique=True,
        max_length=50
    )
    code = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        help_text='회사 종목 코드',
    )    
    
    diff = models.IntegerField(blank=False)
    volume = models.IntegerField(blank=False)