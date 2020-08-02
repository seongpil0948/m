from matplotlib import pyplot as plt
import numpy as np
import datetime
from sklearn.linear_model import LinearRegression


def how_much_increase(origin, target):
    return target / origin -1

def logistic_lr(x_train, x_test, y_train, y_test):
    mlr = LinearRegression()
    mlr.fit(x_train, y_train)
    y_predicted = mlr.predict(x_test)
    plt.scatter(y_test, y_predicted, alpha=0.4)
    plt.xlabel("Actual Rent"); plt.ylabel("Predicted Rent"); plt.title("MULTIPLE LINEAR REGRESSION")
    plt.show()
    return y_predicted