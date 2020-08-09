import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from stock.core.classes import Market
from stock.models import Company

"""
252 = 미국 평균 개장일
"""

# 기업 별 종가 시리즈
"""
codes = [] 
for i in Company.objects.values('code')[:4]: 
    codes.append(i['code']) 
dfs = pd.DataFrame() 
for c in codes: 
    dfs[c] = Market(code=c).get_daily_price['close_price'] 
"""
dfs = pd.DataFrame( # TODO: 다시만들어야 할듯.. 코드는 다른데 값이 같음
    data={
        c['code']: 
            Market(code=c['code']).get_daily_price['close_price']
                for c in Company.objects.values('code')[:4]
    }
)
daily_pct_chg = dfs.pct_change() # percent_change
annual_pct_chg = daily_pct_chg.mean() * 252 

daily_cov = daily_pct_chg.cov() # 공분산
annual_cov = daily_cov * 252
