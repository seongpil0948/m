import datetime
from sklearn.model_selection import train_test_split

from data import get_data
from regression import logistic_lr


# if __name__ == '__main__':
start = datetime.datetime(2020, 1, 1); end = datetime.datetime(2020, 7, 1)
df_prices = get_data(start, end);
df_prices['Date'] = df_prices.index
X = df_prices[['High', 'Low', 'Open', 'Volume', 'Adj Close']]; y = df_prices['Close']
x_train, x_test, y_train, y_test = train_test_split(X, y, train_size=0.8, test_size=0.2)

pred_logistic = logistic_lr(x_train, x_test, y_train, y_test)
