import warnings
from builtins import FutureWarning

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mysqldb import database
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import adfuller

# ignore futureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)


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


# date parser
parsedates = lambda dates: pd.datetime.strptime(dates, "%Y%m").strftime("%Y-%m")

# load all of city name in result table
cities = database.all_city()

dataset = []
for city in cities:
    # loading analysed data
    resultset = pd.read_sql_query(
        "SELECT diagYm as diagym, predictPatients as patients FROM result WHERE diseaseCode = 1 AND city = %s ORDER BY diagym",
        database.connection, params=city)
    # date type convert
    resultset['diagym'] = resultset['diagym'].apply(parsedates)
    resultset.set_index('diagym')

    # check data
    print("=" * 40)
    print("지역: %s" % city)
    data = pd.Series(resultset['patients'].values, index=resultset['diagym'])
    print(data.head())
    print("=" * 40)
    dataset.append(data)

# test_stationartiy(dataset[0])
ts_log = np.log(dataset[0])
ts_log_diff = ts_log - ts_log.shift()
ts_log_diff.dropna(inplace=True)
# plt.plot(ts_log)
# plt.show()

model = ARIMA(ts_log, order=(1, 2, 0))
results_ARIMA = model.fit(disp=-1)
plt.plot(ts_log_diff)
plt.plot(results_ARIMA.fittedvalues, color='red')
plt.title('RSS: %4f' % sum((results_ARIMA.fittedvalues - ts_log_diff) ** 2))
plt.show()


