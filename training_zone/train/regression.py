from tensorflow import keras
# import matplotlib.pyplot as plt
from django.conf import settings
import os
from datetime import datetime
 
from stock.core.strategies.ai.common import get_train_test_data, MinMaxScaler
from stock.core.data import Market


def regression(end=None, start=None, epoch_per_corp=100, batch_size=10):
	m = Market()
	codes = m.get_all_corper_codes
	model = keras.Sequential([
		keras.layers.Dense(units=128, activation='relu'),
		keras.layers.Dense(units=64, activation='relu'),
		keras.layers.Flatten(),
		keras.layers.Dense(units=32, activation='relu'),
		keras.layers.Flatten(),
		keras.layers.Dense(units=16, activation='relu'),
		keras.layers.Flatten(),
		keras.layers.Dense(units=1)
	])
	model.compile(optimizer='adam', loss='mean_squared_error')
	for code in codes:
		try:
			m = Market(code=code)
		except ValueError:
			continue
		raw_df = m.df
		window_size = 1
		if raw_df is None:
				continue
		train_x, train_y, test_x, test_y = get_train_test_data(
			raw_df=raw_df[['close_price']], window_size=window_size, to_float=True
		)
		model.fit(
			train_x, train_y,
			epochs=epoch_per_corp,
			batch_size=batch_size
		)

	model.save(os.path.join(
		settings.TRAINED_MODEL_DIR,
		'regression',
		datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	))

	# y_predicted = model.predict([int(raw_df['close_price'].values[-1])])
	# pred_y = model.predict(test_x)
	# df = MinMaxScaler(raw_df)
	# plt.figure()
	# plt.plot(test_y, color='red', label='real SEC stock price')
	# plt.plot(pred_y, color='blue', label='predicted SEC stock price')
	# plt.title('SEC stock price prediction')
	# plt.xlabel('time')
	# plt.ylabel('stock price')
	# plt.legend()
	# plt.show()    
	# return {
	# 	'predicate': y_predicted.flatten()[0]
	# }
	
if __name__ == "__main__":
  	regression()
	
