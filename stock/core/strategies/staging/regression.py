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
EPOCHS = 1000

train_x, train_y, test_x, test_y = get_train_test_data(raw_df=raw_df, window_size=window_size)
