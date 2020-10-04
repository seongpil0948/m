# import numpy as np
# from tensorflow.keras import models
# from tensorflow.keras.layers import Dense, Activation
# from tensorflow.keras.optimizers import SGD

# from stock.core.networks import large
# from stock.core.common import StockState
# from stock.core.reinforce.experience import prepare_experience


# __all__ = [
#     'QAgent'
# ]


# class QAgent:
#   def __init__(self, window_size, policy='eps-greedy'):
#     self.state = StockState()
#     self.collector = None
#     self.window_size = window_size
#     self.temperature = 0.0
#     self.last_move_value = 0
#     self.policy = policy
  
#   def set_temperature(self, temperature):
#     self.temperature = temperature

#   def set_policy(self, policy):
#       if policy not in ('eps-greedy', 'weighted'):
#           raise ValueError(policy)
#       self.policy = policy

#   def set_model(self, model):
#     self.model = model

#   def set_collector(self, collector):
#     self.collector = collector
  
#   def rank_acts_eps_greedy(self, act_probs):
#     if np.random.random() < self.temperature:
#       np.random.random(act_probs.shape)
#     # the ranks the acts from worst to best
#     ranked_acts =  np.argsort(act_probs)
#     # return best-worst order.
#     return ranked_acts[::-1]

#   def rank_acts_weighted(self, act_probs):
#     p = act_probs / np.sum(act_probs) # 합이 1이되는 수로 정규화 0~1
#     # 1 / 0.3 = 3.333,  0.2 ** 3 =  0.008
#     p = np.power(p, 1.0 / self.temperature)
#     p = p / np.sum(p)
#     return np.random.choice(
#       np.arange(0, len(act_probs)),
#       size=len(act_probs), # 선택개수
#       p=p, # prob distribution
#       replace=False
#     )

#   def select_move(self, state, window_size, column_size):
#     act_probs = self.model.predict([window_size, column_size])
#     np.clip(act_probs, 1e-6, 1-1e-6) # 0 은 허용하지 않겠다
#     # Re-normalization
#     act_probs = act_probs / np.sum(act_probs)
    
#     if self.policy == 'eps-greedy':
#       ranked_acts = self.rank_moves_eps_greedy(act_probs)
#     elif self.policy == 'weighted':
#       ranked_acts = self.rank_moves_weighted(act_probs)
#     else:
#       ranked_acts = None    
#     act = ranked_acts[0]
#     act_idx = state.actions.index(act)

#     # act 에 대한 raward 함수 구현
#     if self.collector is not None:
#       self.collector.record_decision(
#         state=state,
#         action=act
#       )
#     self.last_move_value = float(act_probs[act_idx])
#     return act

#   @property
#   def diagnostics(self):
#       return {'value': self.last_move_value}

#   def train(self, experience, lr, clipnorm, window_size, coumn_size):
#     self.model.compile(
#       loss='categorical_crossentropy',
#       optimizer=SGD(learning_rate=lr, momentum=clipnorm)
#     )
#     n = experience.states.shape[0]
#     y = np.zeros((n,))
#     actions = np.zeros((n, experience.states.shape[1]))
#     for i in range(n):
#       action = experience.actions[i]
#       reward = experience.rewards[i]
#       actions[i][action] = 1
#       y[i] = 1 if reward > 0 else 0    
#     self.model.fit(
#         [experience.states, actions], y,
#         batch_size=window_size,
#         epochs=1)

