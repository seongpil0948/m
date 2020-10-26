import pandas as pd
import matplotlib.pyplot as plt
import datetime
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates

from stock.core.data import Market
from stock.utils.s3 import plt_upload_wrap

__all__ = [
    'tripple_screen'
]

def tripple_screen(*args, **kwargs):
    m = Market(**kwargs)
    df = m.df
    df.index = df.index.map(
        lambda x: datetime.datetime(
            *[int(i) for i in x.split(' ')[0].split('-')]
            )
        )
    def char2date(date):
        return [int(i) for i in date.split('-')]
    """
    ewm: 지수 이동평균 : 12주, 26주
    1. MACD Line
    2. 신호선 9주
    3. macdhist: MACD histogram
    """

    ema60 = df.close_price.ewm(span=60).mean()
    ema130 = df.close_price.ewm(span=130).mean()
    macd = ema60 - ema130 # 1
    signal = macd.ewm(span=45).mean() # 2
    macdhist = macd - signal# 3
    df = df.assign(ema130=ema130, ema60=ema60, macd=macd, signal=signal, macdhist=macdhist).dropna()
    df['number'] = df.index.map(mdates.date2num)
    ohlc = df[['number','open_price','high_price','low_price','close_price']]

    ndays_high = df.high_price.rolling(window=14, min_periods=1).max()
    ndays_low = df.low_price.rolling(window=14, min_periods=1).min()

    fast_k = (df.close_price - ndays_low) / (ndays_high - ndays_low) * 100
    slow_d = fast_k.rolling(window=3).mean()
    df = df.assign(fast_k=fast_k, slow_d=slow_d).dropna()

    plt.figure(figsize=(9, 9))
    p1 = plt.subplot(3, 1, 1)
    plt.title('Triple Screen Trading (NCSOFT)')
    plt.grid(True)
    candlestick_ohlc(p1, ohlc.values, width=.6, colorup='red', colordown='blue')
    p1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.plot(df.number, df['ema130'], color='c', label='EMA130')
    for i in range(1, len(df.close_price)):
        if df.ema130.values[i-1] < df.ema130.values[i] and \
                df.slow_d.values[i-1] >= 20 and df.slow_d.values[i] < 20:
            plt.plot(df.number.values[i], 250000, 'r^') 
        elif df.ema130.values[i-1] > df.ema130.values[i] and \
                df.slow_d.values[i-1] <= 80 and df.slow_d.values[i] > 80:
            plt.plot(df.number.values[i], 250000, 'bv') 
    plt.legend(loc='best')

    p2 = plt.subplot(3, 1, 2)
    plt.grid(True)
    p2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.bar(df.number, df['macdhist'], color='m', label='MACD-Hist')
    plt.plot(df.number, df['macd'], color='b', label='MACD')
    plt.plot(df.number, df['signal'], 'g--', label='MACD-Signal')
    plt.legend(loc='best')

    p3 = plt.subplot(3, 1, 3)
    plt.grid(True)
    p3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.plot(df.number, df['fast_k'], color='c', label='%K')
    plt.plot(df.number, df['slow_d'], color='k', label='%D')
    plt.yticks([0, 20, 80, 100])
    plt.legend(loc='best')

    path = plt_upload_wrap(plt=plt, tech_name=tripple_screen.__name__)
    return path
