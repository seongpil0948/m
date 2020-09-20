__all__ = [
    'StockState'
]

class StockState:
    def __init__(self, budget, num_stocks, raw_df,
        window_size=10, previous_state=None, step=0):
        self.budget = budget # 잔고
        self.num_stocks = num_stocks # 보유 주식수
        self.previous_state = previous_state
        self.window_size = window_size
        self.raw_df = raw_df
        self.df = raw_df[step: self.window_size + step] # window_size 로 슬라이스된 프레임
        self.step = step
        self.actions = ['sell', 'buy', 'hold']

    def valid_action(self, action):
        if action == 'buy':
            return self.budget > self.df[self.step]['close_price']
        elif action == 'sell':
            return self.num_stocks > 0
        else:
            return True

    def apply_action(self, action):
        if action == 'buy':
            self.num_stocks += 1
            self.budget -= self.df[self.step]['close_price']
        elif action == 'sell':
            if self.num_stocks < 1:
                print('you have not enough number of stocks')
        elif action == 'hold':
            pass 
        else:
            return print(f"{action} is not in actions")
        return StockState(
            budget=self.budget,
            num_stocks=self.num_stocks,
            raw_df=self.raw_df,
            window_size=self.window_size,
            previous_state=self, 
            step=self.step + 1
        )
    
    # @property
    # def state(self):
    #     return self.close_prices[
    #         self.step: self.step + self.window_size].extend(
    #             [self.budget, self.])
    @property
    def portfolio(self):
        return self.budget + self.num_stocks * self.close_prices[self.step]

    @property
    def reward(self):
        return self.portfolio - self.previous_state.portfolio


  