import numpy as np
from tensorflow.keras import models
from tensorflow.keras.layers import Dense, Activation, SG
from tensorflow.keras.optimizers import SGD

from stock.core.networks import large
from stock.core.common import StockState, get_train_test_data
from stock.core.reinforce.experience import prepare_experience
from stock.core.data import Market

class PolicyAgent:
  def __init__(self, model, window_size):
    self.model = model
    self.state = StockState
    self.collector = None
    self.window_size = window_size

  def set_collector(self, collector):
    self.collector = collector
    self.collector.begin_episode()

  def select_move(self, game_state, window_size, column_size):
    act_probs = self.model.predict([window_size, column_size])
    np.clip(act_probs, 1e-6, 1-1e-6) # 0 은 허용하지 않겠다
    # Re-normalization
    act_probs = act_probs / np.sum(act_probs)
    act = np.random.choice(game_state.actions, 1, replace=False, p=act_probs)
    if self.collector is not None:
      self.collector.record_decision(
        state=self.state,
        action=act
      )
    return act

  def train(self, experience, lr, clipnorm, window_size, coumn_size):
    self.model.compile(
      loss='categorical_crossentropy',
      optimizer=SGD(learning_rate=lr, momentum=clipnorm)
    )
    target_vectors = prepare_experience(
      experience=experience,
      window_size=self.window_size,
      column_size=coumn_size
    )
    self.model.fit(
      experience.states, target_vectors, window_size, epochs=1
    )

m = Market('2019-01-01', '2019-09-28','207940')
raw_df = m.get_daily_price
window_size = 10 
column_size = 5

# y = 평활화 해야함 (batch_size=window_size, colmun_size) 하지만 close_pirce라 1
train_x, train_y, test_x, test_y = get_train_test_data(raw_df=raw_df, window_size=window_size)
model = models.Sequential()
for layer in large.layers(input_shape=(window_size, column_size, 1)):
  model.add(layer)
model.add(Dense(1))
model.add(Activation('softmax'))
new_agent = PolicyAgent(model)
