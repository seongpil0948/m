""" 
monte carlo policy gradient 

경험데이터 사용 신경망 구축 ->  action에 따른 확률분포 (x) -> action 에따른 결과값 1 or -1 분배 (target or label or y)
-> 차이를 통한 신경망 가중치 경사하강법 사용 -> 확률분포 갱신

"""
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
import numpy as np
import matplotlib.pyplot as plt

from stock.core.data import Market
from .common import get_train_test_data

m = Market('2019-01-01', '2019-09-28','207940')
raw_df = m.get_daily_price

# 10일 간의 데이터를 이용하여 다음날의 종가를 예측한다.
window_size = 10 
# colum size = x[1] size
column_size = 5
train_x, train_y, test_x, test_y = get_train_test_data(raw_df=raw_df, window_size=window_size)

# input_size = [window size, columns length]
model = Sequential()