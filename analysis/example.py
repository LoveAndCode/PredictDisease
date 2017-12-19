import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

rcParams['figure.figsize'] = 15, 6

# define date parser
dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m')

# load time series data
data = pd.read_csv('AirPassengers.csv', parse_dates=['Month'], index_col='Month', date_parser=dateparse)

# check data index
print(data.index)

ts = data['#Passengers']
print(ts.head())


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


test_stationartiy(ts)

# estimating & eliminating trend

ts_log = np.log(ts)
plt.plot(ts_log)
plt.show()

# moving average
moving_average = pd.rolling_mean(ts_log, 12)
plt.plot(ts_log)
plt.plot(moving_average, color='red')
plt.show()

ts_log_moving_avg_diff = ts_log - moving_average

# drop Nan values
ts_log_moving_avg_diff.dropna(inplace=True)
test_stationartiy(ts_log_moving_avg_diff)

# check critical value
print(ts_log_moving_avg_diff.head())

expwighted_avg = pd.ewma(ts_log, halflife=12)

plt.plot(ts_log)
plt.plot(expwighted_avg, color='red')
plt.show()

ts_log_ewma_diff = ts_log - expwighted_avg
test_stationartiy(ts_log_ewma_diff)

ts_log_diff = ts_log - ts_log.shift()
plt.plot(ts_log_diff)
plt.show()

ts_log_diff.dropna(inplace=True)
test_stationartiy(ts_log_diff)

decomposition = seasonal_decompose(ts_log)
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

plt.subplot(411)
plt.plot(ts_log, label='Original')
plt.legend(loc='best')
plt.subplot(412)
plt.plot(trend, label='Trend')
plt.legend(loc='best')
plt.subplot(413)
plt.plot(seasonal, label='Seasonality')
plt.legend(loc='best')
plt.subplot(414)
plt.plot(residual, label='Residuals')
plt.legend(loc='best')
plt.tight_layout()
plt.show()



# Forecasting a Time Series

