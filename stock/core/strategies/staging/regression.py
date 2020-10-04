from stock.core.strategies.ai.common import *
from stock.core.data import Market

import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd

m = Market('2019-01-01', '2019-09-28','207940')
raw_df = m.get_daily_price
window_size = 10
column_size = len(raw_df.columns)

MAX_EPOCHS = 20


# a = keras.preprocessing.timeseries_dataset_from_array(data=raw_df, targets=None, sequence_length=window_size, sequence_stride=1, batch_size=20) 
train_x, train_y, test_x, test_y = get_train_test_data(raw_df=raw_df, window_size=window_size)


# Define Sequential model with 3 layers
model = keras.Sequential(
    [
        layers.Dense(10, activation="relu", name="layer1", input_shape=(window_size, column_size)),
    ]
)
# Call model on a test input
y = model(train_x)

