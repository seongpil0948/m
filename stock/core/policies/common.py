from stock.core.data import Market, get_times

class BasePolicy(Market):
    def __init__(self, budget=10000000, num_stocks=1000,
        code='100220', start_date='2018-01-01', end_date='2019-01-01'):
        self.actions = ['buy', 'sell', 'hold']
        self.budget = budget # 실제로는 API 에서 제공받을 예정
        self.num_stocks = num_stocks
        
        super().__init__(code=code, start_date=start_date, end_date=end_date)

    def go_all_strategies(self):
        df = super().get_daily_price
        print(df)

    def select_action(self):
        pass