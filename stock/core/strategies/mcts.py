import numpy as np
from random import randint
import math

from stock.core.data import Market, get_times
from stock.core.data.codec_json import return_dfs
from stock.core.common.state import StockState

# FIXME: 현재 마지막 노드의 step이 1로 나오는 이유는?


class MCTSNode():
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent # root tree = None
        self.move = move
        self.make_money_counts = 0
        self.num_rollouts = 1
        self.children = []
        self.visited_moves = []
        self.win_count = 0
        # not added at tree yet, if add node, should be added children list 
        self.unvisited_moves = ['sell', 'buy', 'hold']

    def add_rand_child(self):
      idx = randint(0, len(self.unvisited_moves) - 1)
      new_move = self.unvisited_moves.pop(idx)
      if self.state.valid_action(new_move) == False and \
          self.state.num_stocks == 0 :
            new_move = 'buy'
      new_state = self.state.apply_action(new_move)
      new_node = MCTSNode(state=new_state, parent=self, move=new_move)
      self.children.append(new_node)
    
    @property
    def reward(self):
        self.previous_state.portfolio - self.portfolio
    
    @property
    def can_add_child(self):
        return len(self.unvisited_moves) > 0

    def record_win(self):
        self.win_count += 1
        self.num_rollouts += 1

    def record_just(self):
        self.num_rollouts += 1
    @property
    def winning_frac(self):
        return float(self.win_count) / float(self.num_rollouts)


class MCTSAgent:
    def __init__(self, num_rounds, temperature):
        self.num_rounds = num_rounds
        self.temperature = temperature

    def select_child(self, node):
        total_rollouts = sum(child.num_rollouts for child in node.children)
        log_rollouts =  math.log(total_rollouts)
        best_score = -1
        best_child = None

        # each Child
        for child in node.children:
            # Calculate the UCT
            win_percentage = child.winning_frac
            exploreation_factor = math.sqrt(log_rollouts / child.num_rollouts)
            """
            win_count                                 log(total_rollout)
            ------------ * temperature * SquareRoot   ------------------
            num_rollouts                               child.num_rollouts
            """
            uct_score = win_percentage + self.temperature * exploreation_factor
            # check if this is largest we've seen so far
            if uct_score > best_score:
                best_score = uct_score
                best_child = child
        return best_child
    
    def select_move(self, state):
        root = MCTSNode(state)
        for i in range(self.num_rounds):
            node = root
            while not node.can_add_child:
                node = self.select_child(node)

            if node.can_add_child:
                node = node.add_rand_child()
            # winner self.simulate_random_game
            while node is not None:
                if node.reward > 0:
                    node.record_win()
                else:
                    node.record_just()
                node = node.parent
            score_moves = [
                (child.winning_frac, child.move, child.num_rollouts) for child in root.children
            ]
            score_moves.sort(key=lambda x: x[0], reverse=True)
            for s, m, n in score_moves[:10]:
                print(f"{s} {m} {n}")
            # having performed as many MCTS rounds as we have time for, we not pick a move
            best_move = None
            best_pct = -1.0
            for child in root.children:
                child_pct = child.winning_frac
                if child_pct > best_pct:
                    best_pct = child_pct
                    best_move = child.move
            print(f"Select move {best_move} with win pct {best_pct} ")
            return best_move
            


    # @staticmethod
    # def simulate_random_game(game):
    #     bots = {
    #         Player.black: agent.FastRandomBot(),
    #         Player.white: agent.FastRandomBot(),
    #     }
    #     while not game.is_over():
    #         bot_move = bots[game.next_player].select_move(game)
    #         game = game.apply_move(bot_move)
    #     return game.winner()


# if __name__ == '__main__':
dfs = return_dfs(1)
df = dfs[list(dfs.keys())[0]]
prices = df['close_price'].to_list()
column_size = 5
new_game = StockState.new_state(10000000, prices)
bot = MCTSAgent(num_rounds=100, temperature=1.5)

for step in range(len(prices)):
    new_action = bot.select_move(new_game)
    game = new_game.apply_action(new_action, step)
print(game.__dict__)