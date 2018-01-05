import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from math import sqrt
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import adfuller


def test_stationartiy(timeseries):
    # determine rolling statistics
    rolmean = pd.rolling_mean(timeseries, window=12)
    rolstd = pd.rolling_std(timeseries, window=12)

    # plot rolling statistics
    orig = plt.plot(timeseries, color='blue', label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label='Rolling Std')

    # drawing graph
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show()

    # perform Dickey-Fuller test:
    print('Result Of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    for key, value in dftest[4].items():
        dfoutput['Critical Value (%s)' % key] = value
    print('dfoutput : ', dfoutput)


def difference(dataset, interval=1):
    diff = list()
    for i in range(interval, len(dataset)):
        value = dataset[i] - dataset[i - interval]
        diff.append(value)
    return diff


def inverse_difference(history, yhat, interval=1):
    return yhat + history[-interval]


def train_test(datset, plotable=False):
    datset.dropna(inplace=True)
    print("="*60)
    x = datset
    x = x.astype('float32')
    train_size = int(len(x) * 0.50)
    train, test = x[0:train_size], x[train_size:]

    # Walk-Forward
    history = [x for x in train]
    predictions = list()

    for i in range(len(test)):
        # difference data
        month_in_year = 12
        diff = difference(history, month_in_year)

        model = ARIMA(diff, order=(2, 0, 0))
        model_fit = model.fit(trend='nc', disp=0)
        yhat = model_fit.forecast()[0]
        yhat = inverse_difference(history, yhat, month_in_year)
        predictions.append(yhat)
        # observation
        obs = test[i]
        history.append(obs)
        print('>Predicted= %.3f, Expected= %.3f' % (yhat, obs))

    # Report performance
    mse = mean_squared_error(test, predictions)
    rmse = sqrt(mse)
    print('TRAIN_SIZE: %d' % train_size)
    print('TEST: %d' % len(test))
    print('TOTAL: %d' % len(datset.values))
    print('RMSE: %.3f' % rmse)
    if plotable:
        plt.plot(test)
        plt.plot(predictions, color='red')
        plt.title('RSME: %.3f' % rmse)
        plt.show()
    print("="*60)
