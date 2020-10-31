import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout, Flatten
from tensorflow.keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt

from stock.core.data import Market
from stock.core.strategies.ai.common import get_train_test_data, MinMaxScaler


m = Market('2019-01-01', '2019-09-28','207940')
raw_df = m.df
def lstm(raw_df, window_size=10, batch_size=30 , epochs=10):
  train_x, train_y, test_x, test_y = get_train_test_data(raw_df=raw_df, window_size=window_size)
  column_size = train_x.shape[2]
  model = Sequential()
  model.add(LSTM(units=10, activation='relu', return_sequences=True, input_shape=(window_size, column_size)))
  model.add(Dropout(0.1))
  model.add(LSTM(units=10, activation='relu'))
  model.add(Dropout(0.1))
  model.add(Dense(units=1))

  model.compile(optimizer='adam', loss='mean_squared_error')
  model.fit(train_x, train_y, epochs=100, batch_size=30)
  pred_y = model.predict(test_x)
  df = MinMaxScaler(raw_df)

  plt.figure()
  plt.plot(test_y, color='red', label='real SEC stock price')
  plt.plot(pred_y, color='blue', label='predicted SEC stock price')
  plt.title('SEC stock price prediction')
  plt.xlabel('time')
  plt.ylabel('stock price')
  plt.legend()
  plt.show()


  # return next predict date
  return raw_df['close_price'].values[-1] *  pred_y[-1][0] / df['close_price'][-1]

  # for i, p in enumerate(pred_y):
  #     print(p, test_y[i])
  #     print('------>', raw_df.close_price[i], '--->', raw_df.close_price[i+1])
  #     print("Predict tomorrow's  price :", list(raw_df.close_price)[i] * pred_y[i] / list(dfy.close_price)[i], 'KRW')

  # Visualising the results
  """
    plt.figure()
    plt.plot(test_y, color='red', label='real SEC stock price')
    plt.plot(pred_y, color='blue', label='predicted SEC stock price')
    plt.title('SEC stock price prediction')
    plt.xlabel('time')
    plt.ylabel('stock price')
    plt.legend()
    plt.show()

  # raw_df.close[-1] : dfy.close[-1] = x : pred_y[-1]
  """