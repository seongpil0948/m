import numpy as np

from stock.core.common import normalize

def simulate_game(policy):
  player_1_choices = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
  player_1_total = 0
  player_2_choices = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
  player_2_total = 0

  for i in range(100):
    player_1_choice = np.random.choice([1, 2, 3, 4, 5], p=policy)
    player_1_choices[player_1_choice] += 1
    player_1_total += player_1_choice

    player_2_choice = np.random.choice([1, 2, 3, 4, 5], p=policy)
    player_2_choices[player_2_choice] += 1
    player_2_total += player_2_choice

  if player_1_total > player_2_total:
    winner = player_1_choices
    loser = player_2_choices
  else:
    winner = player_2_choices
    loser = player_1_choices
  return (winner, loser)

choices = [1, 2, 3, 4, 5]
policy = np.array([0.2, 0.2, 0.2, 0.2, 0.2])
lr = 0.0001
num_games = 1000
for i in range(num_games):
  winner, loser = simulate_game(policy)
  for j, choice in enumerate(choices):
    # 이긴 놈은 가장 큰수를 진놈보다 많이 뽑았을 것이다 고로 양수가 나올 것이다
    # else: 음수가 나올 것이다 그럼 확률도 줄어들 것이다.
    net_wins = winner[choice] - loser[choice]
    policy[j] += lr * net_wins
  policy = normalize(policy)
  print(f" epoch {i} \n policy = {policy}")


# ================================================
exp_length = 100
total_return = discounted_return = reward = {}

for exp_idx in range(exp_length):
  total_return[exp_idx] = reward[exp_idx]
  discount_amount = 0.75
  # 마래로 가면 갈수록 보상의 영향을 적게 받는다.
  for future_reward_idx in range(exp_idx + 1, exp_length):
    discounted_return[exp_idx] += discount_amount * reward[future_reward_idx]
  discount_amount *= 0.75