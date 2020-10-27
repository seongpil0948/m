import matplotlib.pyplot as plt

from stock.core.data import Market
from stock.models import Company, get_all_corper
from stock.utils.s3 import plt_upload_wrap

"""
반전 매매기법: 주가가 반전하는 지점을 찾아내 매수 혹은 매도
1. II: intraday intensity= 일중강도 = (1 ~ 0 ~ -1) 
    %b < 0.05 , II > 0 (강세지표 증가) => 매수
2. 일중 강도율 퍼센트

볼린저 밴드를 확증하는 도구: 주가가 하단 밴드에 닿을때 강도가 > 0 이면 매수 반대는 매도 조언
매수 = 빨강 , 매도 파랑
"""

__all__ = [
    'bolinger_reversal'
    ]


def bolinger_reversal(*args, **kwargs):
    window_size = kwargs.pop('window_size', None)
    m = Market(**kwargs)
    m.add_rolling(window_size=window_size)
    df = m.df

    df['upper'] = df['MAvg'] + (df['STD'] * 2)
    df['lower'] = df['MAvg'] - (df['STD'] * 2)
    df['PB'] = (df['close_price'] - df['lower']) / (df['upper'] - df['lower'])

    df['II'] = ( 
        2 * df['close_price'] - df['high_price'] - df['low_price']
        ) / (
        df['high_price'] - df['low_price'] 
        ) * df['volume']  # ①
    df['IIP21'] = df['II'].rolling(window=21).sum() / df['volume'].rolling(window=21).sum()*100  # ②
    df = df.dropna()

    plt.figure(figsize=(9, 9))
    plt.subplot(3, 1, 1)
    plt.title('Bollinger Band(20 day, 2 std) - Reversals')
    plt.plot(df.index, df['close_price'], 'b', label='close_price')
    plt.plot(df.index, df['upper'], 'r--', label ='Upper band')
    plt.plot(df.index, df['MAvg'], 'k--', label='Moving average 20')
    plt.plot(df.index, df['lower'], 'c--', label ='Lower band')
    plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')

    for i in range(0, len(df.close_price)):
        if df.PB.values[i] < 0.05 and df.IIP21.values[i] > 0:   
            plt.plot(df.index.values[i], df.close_price.values[i], 'r^')
        elif df.PB.values[i] > 0.95 and df.IIP21.values[i] < 0: 
            plt.plot(df.index.values[i], df.close_price.values[i], 'bv')

    plt.legend(loc='best')
    plt.subplot(3, 1, 2)
    plt.plot(df.index, df['PB'], 'b', label='%b')
    plt.grid(True)
    plt.legend(loc='best')

    plt.subplot(3, 1, 3)  # ③
    plt.bar(df.index, df['IIP21'], color='g', label='II% 21day')  # ④
    plt.grid(True)
    plt.legend(loc='best')

    path = plt_upload_wrap(plt=plt, tech_name=bolinger_reversal.__name__)
    return path