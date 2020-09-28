# import argparse
# import h5py
# from tensorflow.keras.layers import Dense, Input, concatenate
# from tensorflow.keras.models import Model

# from stock.core import networks
# from stock.core import reinforce as rl
# from stock.core.data import Market
# from stock.core.common import StockState, get_train_test_data
# from stock.core.reinforce import QAgent


# window_size =  10
# start_date = '2019-01-01'
# end_date =  '2020-01-01'
# item_code = '207940'
# network = 'large'
# hidden_size =  512

# m = Market(start_date=start_date, end_date=end_date, code=item_code)
# raw_df = m.get_daily_price
# window_size = window_size
# column_size = 5
# init_agent = QAgent(window_size)

# prices_input = Input(shape=(window_size, column_size), name='prices_input')
# # TODO: (3, 0) zero padding 필요할듯
# action_input = Input(shape=(len(init_agent.state.actions),), name='action_input')
# processed = prices_input
# # networks.__dict__ 에서 가져와야 한다.
# network = getattr(networks, network)
# breakpoint()

# for layer in network.layers(input_shape=(window_size, column_size)):
#     processed = layer(processed)

# breakpoint()
# board_plus_action = concatenate([action_input, processed])
# hidden_layer = Dense(hidden_size, activation='relu')(board_plus_action)
# value_output = Dense(1, activation='sigmoid')(hidden_layer)

# breakpoint()
# model = Model(inputs=[prices_input, action_input], outputs=value_output)
# new_agent = init_agent.set_model(model).set

