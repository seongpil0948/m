import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
import numpy as np
import matplotlib.pyplot as plt

from stock.core.data import Market
from stock.core.common import get_train_test_data, MinMaxScaler


m = Market('2019-01-01', '2019-09-28','207940')
raw_df = m.get_daily_price

# 10일 간의 데이터를 이용하여 다음날의 종가를 예측한다.
window_size = 10 
# colum size = x[1] size
column_size = 5

train_x, train_y, test_x, test_y = get_train_test_data(raw_df=raw_df, window_size=window_size)
# input_size = [window size, columns length]
model = Sequential()
model.add(LSTM(units=10, activation='relu', return_sequences=True, input_shape=(window_size, column_size)))
model.add(Dropout(0.1))
model.add(LSTM(units=10, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(units=1))
model.summary()

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(train_x, train_y, epochs=60, batch_size=30)
pred_y = model.predict(test_x)
print(len(pred_y), len(test_x), len(test_y))
score = model.evaluate(test_x, test_y, verbose=0)
# dfx = raw_df[['open_price', 'high_price', 'low_price', 'close_price', 'volume']]
# dfx = MinMaxScaler(dfx)
# dfy = dfx[['close_price']]

# for i, p in enumerate(pred_y):
#     print(p, test_y[i])
#     print('------>', raw_df.close_price[i], '--->', raw_df.close_price[i+1])
#     print("Predict tomorrow's  price :", list(raw_df.close_price)[i] * pred_y[i] / list(dfy.close_price)[i], 'KRW')

# Visualising the results
"""print(pred_y)
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