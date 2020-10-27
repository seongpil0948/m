import io
import uuid
import boto3
import matplotlib.pyplot as plt

from django.conf import settings
from stock.core.data import Market
from stock.utils.s3 import plt_upload_wrap
"""
볼린저 밴드는 다음과 같이 구성된다.
    1. N기간 동안의 이동평균(MA)
    2. 이동평균 위의 K배 표준편차 상위 밴드
    3. 이동평균 아래의 K배 표준편차 하위 밴드
    4. 일반적으로 N과 K의 값은 20과 2이다. 평균값의 기본 선택의 단순 이동 평균이지만,
        필요에 따라 다른 종류의 평균값을 쓸 수 있다.
        지수 이동 평균(Exponential moving averages)은 일반적인 대안이다.
        대개 중간 밴드와 표준 편차의 계산을 위해 같은 기간을 사용한다.

1. percentB = 주가가 상단 밴드에 위치시 1.0, 중간 0.5, 하단 0 
2. 밴드사이의 폭을 의미 = 스퀴즈 확인 = 변동성이 극히 낮아지며 곧이어 확 높아지는 변동성을 예상
    추세의 시작과 마지막을 포착 하며 강한 상승세 일경우 하단 볼린저 밴드가 확 낮아진다
    u - 2std 를 감안 해보면 당연하다. 

"""

__all__ = ['bolinger_band']

def bolinger_band(*args, **kwargs):
    window_size = kwargs.pop('window_size', None)
    m = Market(**kwargs)
    m.add_rolling(window_size=window_size)
    df = m.df

    df['upper'] = df['MAvg'] + (df['STD'] * 2)
    df['lower'] = df['MAvg'] - (df['STD'] * 2)
    df['PB'] = (df['close_price'] - df['lower']) / (df['upper'] - df['lower']) # 1
    df['bandwidth'] = (df['upper'] - df['lower']) / df['MAvg'] * 100 # 2

    """
    현금 흐름(Money Flow) = 중심 가격 * 거래량
    MFI = Money Flow Index(지표) 가격과 거래량 동시분석
        80 상회 : 강력매수 
        20 하회: 강력 매도 
    RMF = TP 가 전날보다 상승한 현금 흐름의 합

    1 매수: %b > 0.8 and MFI > 80 빨강 삼각형
    3 매도: %b < 0.2 and MFI > 20 파란 삼각형
    5 MFI 와 비교를 위해 100을 곱해서 푸른색 실선
    """
    # typical price 중심가격
    df['TP'] = (df['high_price'] + df['low_price'] + df['close_price']) / 3 
    df['PMF'] = 0 # positive money flow
    df['NMF'] = 0 # negative
    for i in range(len(df.close_price)-1):
        if df.TP.values[i] < df.TP.values[i+1]:
            df.PMF.values[i+1] = df.TP.values[i+1] * df.volume.values[i+1]
            df.NMF.values[i+1] = 0
        else:
            df.NMF.values[i+1] = df.TP.values[i+1] * df.volume.values[i+1]
            df.PMF.values[i+1] = 0
    # Money Flow Ratio 현금흐름 비율
    df['MFR'] = df.PMF.rolling(window=20).sum() / df.NMF.rolling(window=20).sum()
    # Money Flow Index
    df['MFI20'] = 100 - 100 / (1 + df['MFR'])

    plt.figure(figsize=(9, 5)) 
    plt.plot(df.index, df['close_price'], color='#0000ff', label='close_price')
    plt.plot(df.index, df['upper'], 'r--', label = 'Upper band')      
    plt.plot(df.index, df['MAvg'], 'k--', label='Moving average 20') 
    plt.plot(df.index, df['lower'], 'c--', label = 'Lower band')
    plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')
    for i in range(len(df.close_price)):
        if df.PB.values[i] > 0.8 and df.MFI20.values[i] > 80:       # ①
            plt.plot(df.index.values[i], df.close_price.values[i], 'r^')  
        elif df.PB.values[i] < 0.2 and df.MFI20.values[i] < 20:     # ③
            plt.plot(df.index.values[i], df.close_price.values[i], 'bv')  
    plt.legend(loc='best') 
    plt.title('Bollinger Band (20 day, 2 std)') 

    plt.subplot(2, 1, 1)
    plt.plot(df.index, df['bandwidth'], color='m', label='BandWidth')
    plt.grid(True)
    plt.legend(loc='best')

    plt.subplot(2, 1, 2)
    plt.plot(df.index, df['PB'] * 100, 'b', label='%B x 100')       # ⑤ 
    plt.plot(df.index, df['MFI20'], 'g--', label='MFI(20 day)')     # ⑥
    plt.yticks([-20, 0, 20, 40, 60, 80, 100, 120])                  # ⑦
    for i in range(len(df.close_price)):
        if df.PB.values[i] > 0.8 and df.MFI20.values[i] > 80:
            plt.plot(df.index.values[i], 0, 'r^')
        elif df.PB.values[i] < 0.2 and df.MFI20.values[i] < 20:
            plt.plot(df.index.values[i], 0, 'bv')
    plt.grid(True)
    plt.legend(loc='best')

    path = plt_upload_wrap(plt=plt, tech_name=bolinger_band.__name__)
    return path
    
    
    
    
    






    