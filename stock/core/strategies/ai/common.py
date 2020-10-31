import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tensorflow import keras


__all__ = [
    'MinMaxScaler',
    'get_train_test_data',
    'normalize',
    'plot_history',
    'stat',
]

def plot_history(history):
  # history = result of fit
  hist = pd.DataFrame(history.history)
  hist['epoch'] = history.epoch

  plt.figure(figsize=(8,12))

  plt.subplot(2,1,1)
  plt.xlabel('Epoch')
  plt.ylabel('Mean Abs Error [MPG]')
  plt.plot(hist['epoch'], hist['mae'],
           label='Train Error')
  plt.plot(hist['epoch'], hist['val_mae'],
           label = 'Val Error')
  plt.ylim([0,5])
  plt.legend()

  plt.subplot(2,1,2)
  plt.xlabel('Epoch')
  plt.ylabel('Mean Square Error [$MPG^2$]')
  plt.plot(hist['epoch'], hist['mse'],
           label='Train Error')
  plt.plot(hist['epoch'], hist['val_mse'],
           label = 'Val Error')
  plt.ylim([0,20])
  plt.legend()
  plt.show()

def stat(df):
    return df.describe().transpose()

def norm(df, mean, std):
  return (df - mean) / std

# prob distribute
def normalize(policy):
    policy = np.clip(policy, 0, 1)
    return policy / sum(policy)

def MinMaxScaler(data):
    """최솟값과 최댓값을 이용하여 0 ~ 1 값으로 변환"""
    numerator = data - np.min(data, 0) # 분자 
    denominator = np.max(data, 0) - np.min(data, 0) # 분모
    # 0으로 나누기 에러가 발생하지 않도록 매우 작은 값(1e-7)을 더해서 나눔
    return numerator / (denominator + 1e-7)

def get_train_test_data(raw_df, window_size, to_float=True, train_test_ratio=0.7):
    dfx = raw_df
    # dfx = raw_df[['open_price', 'high_price', 'low_price', 'close_price', 'volume']]
    if to_float:
      dfx = MinMaxScaler(dfx)
    dfy = dfx[['close_price']]

    x = dfx.values.tolist()
    y = dfy.values.tolist()

    data_x = []
    data_y = []
    for i in range(len(y) - window_size):
        _x = x[i : i + window_size] # 다음 날 종가(i+windows_size)는 포함되지 않음
        _y = y[i + window_size]     # 다음 날 종가
        data_x.append(_x)
        data_y.append(_y)
    print(_x, "->", _y)

    train_size = int(len(data_y) * train_test_ratio)
    train_x = np.array(data_x[0 : train_size])
    train_y = np.array(data_y[0 : train_size])

    test_size = len(data_y) - train_size
    test_x = np.array(data_x[train_size : len(data_x)])
    test_y = np.array(data_y[train_size : len(data_y)])    

    return train_x, train_y, test_x, test_y