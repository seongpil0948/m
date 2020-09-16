import argparse
import h5py
from tensorflow.keras.layers import Dense, Input, concatenate
from tensorflow.keras.models import Model

from stock.core import networks
from stock.core import reinforce as rl
from stock.core.data import Market
from stock.core.common import StockState, get_train_test_data
from stock.core.reinforce import QAgent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--window_size', type=int, default=10)
    parser.add_argument('--start-date', type=str, default='2019-01-01')
    parser.add_argument('--end-date', type=str, default='2020-01-01')
    parser.add_argument('--item-code', type=str, default='207940')
    parser.add_argument('--network', default='large')
    parser.add_argument('--hidden-size', type=int, default=512)
    parser.add_argument('output_file')
    args = parser.parse_args()

    m = Market(start_date=args.start-date, end_date=args.end-date, code=args.item-code)
    raw_df = m.get_daily_price
    window_size = args.window_size
    column_size = 5
    init_agent = QAgent(window_size)

    prices_input = Input(shape=(window_size, column_size), name='prices_input')
    # TODO: (3, 0) zero padding 필요할듯
    action_input = Input(shape=(len(init_agent.state.actions),), name='action_input')

    processed = prices_input
    # networks.__dict__ 에서 가져와야 한다.
    network = getattr(networks, args.network)
    for layer in network.layers(input_shape=(window_size, column_size)):
        processed = layer(processed)

    board_plus_action = concatenate([action_input, processed])
    hidden_layer = Dense(args.hidden_size, activation='relu')(board_plus_action)
    value_output = Dense(1, activation='sigmoid')(hidden_layer)

    model = Model(inputs=[prices_input, action_input], outputs=value_output)
    new_agent = init_agent.set_model(model).set


if __name__ == '__main__':
    main()
