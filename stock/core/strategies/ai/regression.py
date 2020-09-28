from stock.core.strategies.ai.common import *
from stock.core.data import Market

import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd


" FIXME: 현재 네트워크의 결과값이  1이 나와야하는데 여러 차원이 나오는중 ..."
def build_model():
  model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=[window_size, len(raw_df.columns)]),
    layers.Dense(64, activation='relu'),
    layers.Dense(1)
  ])

  optimizer = tf.keras.optimizers.RMSprop(0.001)

  model.compile(loss='mse',
                optimizer=optimizer,
                metrics=['mae', 'mse'])
  return model

m = Market('2019-01-01', '2019-09-28','207940')
raw_df = m.get_daily_price
window_size = 10
column_size = len(raw_df.columns)
EPOCHS = 1000

train_x, train_y, test_x, test_y = get_train_test_data(raw_df=raw_df, window_size=window_size)
model = build_model()
model.summary()

# patience 매개변수는 성능 향상을 체크할 에포크 횟수입니다
early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)

history = model.fit(train_x, train_y, epochs=EPOCHS,
                    validation_split = 0.2, verbose=0, callbacks=[early_stop, PrintDot()])

# plot_history(history)
# evaluate
loss, mae, mse = model.evaluate(test_x, test_y, verbose=2)

print("테스트 세트의 평균 절대 오차: {:5.2f} MPG".format(mae))
test_predictions = model.predict(test_x).flatten()
breakpoint()


plt.scatter(test_y, test_predictions)
plt.xlabel('True Values [MPG]')
plt.ylabel('Predictions [MPG]')
plt.axis('equal')
plt.axis('square')
plt.xlim([0,plt.xlim()[1]])
plt.ylim([0,plt.ylim()[1]])
_ = plt.plot([-100, 100], [-100, 100])