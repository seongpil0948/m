__all__ = [
    'StockState'
]

class StockState:
    def __init__(self, budget, num_stocks,
        previous_state, close_prices, step):
        self.budget = budget # 잔고
        self.num_stocks = num_stocks # 보유 주식수
        self.previous_state = previous_state
        self.close_prices = close_prices # 일별 종가 리스트
        self.step = step
        self.actions = ['sell', 'buy', 'hold']

    def valid_action(self, action):
        if action == 'buy':
            return self.budget > self.close_prices[self.step]
        elif action == 'sell':
            return self.num_stocks > 0
        else:
            return True

    def apply_action(self, action):
        if action == 'buy':
            self.num_stocks += 1
            self.budget -= self.close_prices[self.step]
        elif action == 'sell':
            if self.num_stocks < 1:
                print('you have not enough number of stocks')
        elif action == 'hold':
            pass 
        else:
            return print(f"{action} is not in actions")
        return StockState(
            self.budget,
            self.num_stocks,
            self, 
            self.close_prices,
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

    @staticmethod
    def new_state(budget, close_prices):
        return StockState(
            budget=budget,
            close_prices=close_prices,
            num_stocks=0,
            previous_state=None,
            step=0
        )



  