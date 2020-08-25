from stock.core.data import Market, get_times
import numpy as np


class QLearningDecisionPolicy(Market):
    def __init__(self, budget=10000000, num_stocks=1000, stock_price=100,
        code='100220', start_date='2018-01-01', end_date='2019-01-01', prices=[]):
        self.actions = ['buy', 'sell', 'hold']
        self.budget = budget # 실제로는 API 에서 제공받을 예정
        self.num_stocks = num_stocks
        self.stock_price = stock_price
        self.prices = prices # super().get_daily_price
        super().__init__(code=code, start_date=start_date, end_date=end_date)

    def select_action(self, step):
        threshold = min(self.epsilon, step / 1000.)
        """if np.random.rand() < threshold:         
            # Exploit best option with probability epsilon
                action_q_vals = self.sess.run(self.q, feed_dict={self.x: current_state})
                action_idx = np.argmax(action_q_vals)  # TODO: replace w/ tensorflow's argmax
                action = self.actions[action_idx]
        else:"""
        # Explore random option with probability 1 - epsilon
        action = self.actions[np.random.randint(0, len(self.actions) - 1)]
        return action
    
    def run_simulation(self, action, target_count, window_size):
        if target_count == 'all':
            count = self.budget / self.stock_price

        for i in range(len(self.prices)):
            if i % 100 == 0:
                print('progress {:.2f}%'.format(float(100*i) / (len(self.prices) - window_size - 1)))
            transtions = []
            curr_state = [self.prices[i: i + window_size].extend([self.budget, self.num_stocks])]
            current_portfolio = self.budget + self.num_stocks * self.stock_price
            if action not in self.actions:
                print(f"{action} is not exist")
            elif action == 'buy':
                self.num_stocks += count
                self.budget = self.budget % self.stock_price
            elif action == 'sell' and self.num_stocks > 0:
                self.budget += self.stock_price * count
                self.num_stocks -= 1 * count
            else:
                action = 'hold'        
            new_portfolio = self.budget + self.num_stocks * self.stock_price
            reward = new_portfolio - current_portfolio
            next_state = [self.prices[i: i + window_size].extend([self.budget, self.num_stocks])]
            transtions.append((curr_state, action, reward, next_state))

            # TODO: Q 구현 ㄲ policy.update_q(current_state, action, reward, next_state)

        portfolio = self.budget + self.num_stocks * self.stock_price
        return portfolio

    def run_simulations(self, num_tries=10):
        window_size = 10
        final_portfolios = []
        target_count = 'all'
        for i in range(num_tries):
            action = self.select_action(step=i)
            final_portfolio = run_simulation(action=action, target_count=target_count, window_size=window_size)
            final_portfolios.append(final_portfolio)
        avg, std = np.mean(final_portfolios), np.std(final_portfolios)
        return avg, std