import pandas_datareader as pdr
import datetime

__all__ = [
    'get_data'
]

def get_data(start, end):
    """
    High 최고가 Low 최저가 Open 시가 Close 종가 Volume 거래량 Adj Close 수정종가 
    KS = 코스닥, KQ = 코스피
    """
    gs = pdr.data.DataReader("078930.KS", "yahoo", start, end)
    msft = pdr.get_data_yahoo('msft', start, end)
    samsung_electronic = pdr.get_data_yahoo('005930.KS', start, end)
    return gs
