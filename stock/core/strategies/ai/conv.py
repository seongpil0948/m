# import numpy as np
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, MaxPooling2D
# from tensorflow.keras.layers import Conv2D, Flatten, Dropout

# from stock.core.data.codec_json import return_dfs
# from stock.core.strategies.ai import get_train_test_data
# from stock.core.data import Market


# # dfs = return_dfs(1)
# # raw_df = dfs[list(dfs.keys())[0]]

# m = Market('2019-01-01', '2019-09-28','207940')
# raw_df = m.get_daily_price
# # 10일 간의 데이터를 이용하여 다음날의 종가를 예측한다.
# window_size = 10 
# # colum size = x[1] size
# column_size = 5

# # y = 평활화 해야함 (batch_size=window_size, colmun_size) 하지만 close_pirce라 1
# train_x, train_y, test_x, test_y = get_train_test_data(raw_df=raw_df, window_size=window_size)
# train_x = train_x.reshape(-1, window_size, column_size, 1)
# test_x = test_x.reshape(-1, window_size, column_size, 1)
# train_y = train_y.reshape(-1, 1, 1, 1)
# test_y = test_y.reshape(-1, 1, 1, 1)
# model = Sequential()
# model.add(Conv2D(
#   filters=16,
#   kernel_size=(2, 2),  
#   activation='sigmoid',
#   input_shape=(window_size, column_size, 1)))
# model.add(Dropout(rate=0.6))
# model.add(Conv2D(32, (2, 2), activation='sigmoid'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(Dropout(rate=0.6))
# model.add(Flatten())
# model.add(Dense(64, activation='sigmoid'))
# model.add(Dropout(rate=0.6))
# model.add(Dense(1, activation='sigmoid'))
# model.summary()

# # categorical_crossentropy
# model.compile(loss='mean_squared_error',
#               optimizer='sgd',
#               metrics=['accuracy'])

# model.fit(train_x, train_y,
#           batch_size=64,
#           epochs=1000,
#           verbose=1,
#           validation_data=(test_x, test_y))

# score = model.evaluate(test_x, test_y, verbose=0)
# print('Test loss:', score[0])
# print('Test accuracy:', score[1])