# import random
# import tensorflow as tf
# import numpy as np

# from stock.core.strategies import sp_lstm
# from stock.core.data import Market
# from stock.core.common import StockState

# class QLearningDecisionPolicy:
#   def __init__(self, budget=100000, num_stocks=100,
#    start_date='2019-01-01', end_date='2019-09-28', code='207940'):
#       self.epsilon = 0.9
#       self.gamma = 0.001
#       self.alpha = 0.06
#       self.actions = ['sell', 'buy', 'hold']
#       self.m = Market(start_date=start_date, end_date=end_date, code=code)
#       self.raw_df = self.m.get_daily_price
#       self.all_prices = self.m.close_prices
#       self.state = StockState(budget=budget, num_stocks=num_stocks, raw_df=self.raw_df)
#       self.num_tries = 10
#       self.window_size = 10
#       self.transitions = []
#       self.curr_action_q_vals = []
  
#   def select_action(self, step):
#     # epsilon 이하 까지는 점점 탐험 확률이 내려간다
#     # FIXME: All price가 아니라 현재 State로 훈련을 해야한다.. 현재 State에 아무값도 안들어가는중
#     # TODO: 슬라이싱된 df 가 정상적으로 돌아갈지..
#     threshold = min(self.epsilon, step / 1000.)
#     if random.random() < threshold:
#       self.curr_action_q_vals = sp_lstm(df=self.state.df)
#       action_idx = np.argmax(np.sum(self.curr_action_q_vals, axis=0))
#       action = self.actions[action_idx]
#     else:
#       action = self.actions[random.randint(0, len(self.actions) - 1)]
#     return action

#   def run_simulation(self, debug=False):
#       share_value = 0
#       transitions = list()
#       for i in range(len(self.all_prices) - self.window_size - 1):
#           if i % 100 == 0:
#             print('progress {:.2f}%'.format(float(100*i) / (len(self.all_prices) - self.window_size - 1)))
#           old_raward = self.state.reward
#           action = self.select_action(step=i)
#           new_state =  self.state.apply_action(action)
#           new_reward = new_state.reward
#           self.q = (1 - self.alpha) * old_raward + self.alpha * new_reward
#           self.state = new_state
#           self.transitions.append((self.state.previous_state, action, q , self.state))
#       portfolio = self.state.portfolio # last
#       if debug:
#           print(f" portfolio ==> budget :{self.state.budget} \n numstocks: {self.state.num_stocks}")
#       return portfolio

#   def run_simulations(self):
#     final_portfolios = list()
#     for i in range(num_tries):
#         final_portfolio = self.run_simulation()
#         final_portfolios.append(final_portfolio)
#     avg, std = np.mean(final_portfolios), np.std(final_portfolios)
#     return avg, std    



# agent = QLearningDecisionPolicy()
# action = agent.select_action(step=0)
# print(action)