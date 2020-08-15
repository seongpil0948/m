class BasePolicy:
    def __init__(self, budget, num_stocks, code):
        self.actions = ['buy', 'sell', 'hold']
        self.budget = budget
        self.num_stocks = num_stocks
        self.code = code

    def select_action(self):
        pass