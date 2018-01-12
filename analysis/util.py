from math import sqrt

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager, rc
from sklearn.metrics import mean_squared_error
from statsmodels.graphics.tsaplots import plot_pacf, plot_acf
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import adfuller

# Korean Character Encoding For matplotlib
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/나눔고딕코딩.ttf").get_name()
rc('font', family=font_name)
print(font_name)

# Matplotlib plot Configuration
plt.rcParams['figure.figsize'] = (14, 5)
plt.rcParams['figure.dpi'] = 100

cityDic = {'서울특별시': "Seoul", "광주광역시": "GwangJu", "대구광역시": "DaeGu", "대전광역시": "DaeJeon", "부산광역시": "Busan",
           "울산광역시": "Ulsan", "인천광역시": "Incheon", "청주시": "CheongJu"}


def acf_pacf(dataset):
    # ts_log = np.log(dataset)
    ts_log = dataset
    ax1 = plt.subplot(211)
    plot_acf(ts_log, ax=ax1)
    ax2 = plt.subplot(212)
    plot_pacf(ts_log, ax=ax2)
    plt.tight_layout()
    plt.savefig("..\graph\ACF_PACF.png", format='png')
    plt.show()


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


def train_test(datset, city, plotable=False):
    datset.dropna(inplace=True)

    # Check optimal parameter for ARIMA Model
    acf_pacf(datset)

    print("=" * 60)
    x = datset
    x = x.astype('float32')
    # 80% data use for train data
    train_size = int(len(x) * 0.80)
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
    print('City: %s' % city)
    print('TRAIN_SIZE: %d' % train_size)
    print('TEST: %d' % len(test))
    print('TOTAL: %d' % len(datset.values))
    print('RMSE: %.3f' % rmse)
    if plotable:
        plt.plot(test, marker='D', label='Real Data')
        plt.plot(predictions, color='red', marker='s', label='Predict Data')
        plt.legend()
        plt.title('CityName: %s  RSME: %.3f' % (cityDic[city[0]], rmse))
        plt.xlabel('Date')
        plt.ylabel('Number of Patients')
        plt.savefig("..\graph\important_city\%s.png" % city[0], format='png')
        plt.show()
    print("=" * 60)
    dic = {"realData": test, "predictData": predictions}
    pd.DataFrame(dic).to_csv("..\graph\important_city\%s.csv" % city[0], sep=",", na_rep='NaN')
