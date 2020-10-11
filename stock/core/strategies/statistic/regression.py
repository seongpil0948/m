from sklearn.linear_model import LinearRegression

from stock.core.strategies.ai.common import get_train_test_data
from stock.core.data import Market
from stock.core.data.codec_json import return_dfs


def regression(code='207940', end='2019-09-28', start='2019-01-01'):
    m = Market(start_date=start, end_date=end, code=code)
    raw_df = m.get_daily_price
    # raw_df = return_dfs()
    # raw_df = raw_df[list(raw_df.keys())[0]  ]
    window_size = 1

    # a = keras.preprocessing.timeseries_dataset_from_array(data=raw_df, targets=None, sequence_length=window_size, sequence_stride=1, batch_size=20) 
    train_x, train_y, test_x, test_y = get_train_test_data(raw_df=raw_df[['close_price']], window_size=window_size, to_float=False)

    # fit() 메서드는 선형 회귀 모델에 필요한 두 가지 변수를 전달하는 거다.
    line_fitter = LinearRegression()
    line_fitter.fit(train_x.reshape(-1, 1) , train_y.reshape(-1, 1))
    y_predicted = line_fitter.predict([[raw_df['close_price'].values[-1]]]) 
    return {
        'coef': line_fitter.coef_,
        'intercept': line_fitter.intercept_,
        'predicate': y_predicted

    }
    
    
