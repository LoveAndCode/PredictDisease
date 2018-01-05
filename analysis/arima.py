import warnings
from builtins import FutureWarning
import pandas as pd
from sklearn.metrics import mean_squared_error
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt

from analysis import util
from mysqldb import database
from statsmodels.tsa.arima_model import ARIMA

# ignore futureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

# load all of city name in result table
cities = database.all_city()

# date parser
parsedates = lambda dates: pd.datetime.strptime(dates, "%Y%m").strftime("%Y-%m")

# total dataSet
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

#
# util.test_stationartiy(dataset[0])
# ts_log = np.log(dataset[0])
# ts_log_diff = ts_log - ts_log.shift()
# ts_log_diff.dropna(inplace=True)
# # plt.plot(ts_log)
# # plt.show()
#
# model = ARIMA(ts_log, order=(1, 1, 0))
# results_ARIMA = model.fit(disp=1)
# plt.plot(ts_log_diff, color='green')
# plt.plot(results_ARIMA.fittedvalues, color='red')
# plt.title('RSS: %.4f' % sum((results_ARIMA.fittedvalues - ts_log_diff) ** 2))
# plt.show()
#
# predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)
# predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()
# print(predictions_ARIMA_diff_cumsum.head())
#
# predictions_ARIMA_log = pd.Series(ts_log.ix[0], index=ts_log.index)
# predictions_ARIMA_log = predictions_ARIMA_log.add(predictions_ARIMA_diff_cumsum, fill_value=0)
# print(predictions_ARIMA_log.head())
#
# predictions_ARIMA = np.exp(predictions_ARIMA_log)
# plt.plot(dataset[0])
# plt.plot(predictions_ARIMA)
# plt.title('RMSE: %.4f' % np.sqrt(sum((predictions_ARIMA - dataset[0]) ** 2) / len(dataset[0])))
# plt.show()
#
# result = dataset[0]
# result['y'] = np.log(dataset[0])
# # plt.plot(result, color='RED')
# # plt.show()
# print(result)
#
# # print(dataset[0].index)



# Prepare Data

# x = dataset[1]
# x = x.astype('float32')
# train_size = int(len(x) * 0.50)
# train, test = x[0:train_size], x[train_size:]
#
# # Walk-Forward validation
# history = [x for x in train]
# predictions = list()
#
# for i in range(len(test)):
#     # difference data
#     month_in_year = 12
#     diff = util.difference(history, month_in_year)
#     # predict
#     # 2,1,0 => RMSE : 6978
#     # 2,0,0 => RMSE : 6921
#
#     model = ARIMA(diff, order=(2, 0, 0))
#     model_fit = model.fit(trend='nc', disp=0)
#     yhat = model_fit.forecast()[0]
#     yhat = util.inverse_difference(history, yhat, month_in_year)
#     predictions.append(yhat)
#     # observation
#     obs = test[i]
#     history.append(obs)
#     print('>Predicted= %.3f, Expected= %.3f' % (yhat, obs))
#
# # Report performance
# mse = mean_squared_error(test, predictions)
# rmse = sqrt(mse)
#
# print('TRAIN_SIZE: %d' % train_size)
# print('TEST: %d' % len(test))
# print('TOTAL: %d' % len(dataset[1].values))
# print('RMSE: %.3f' % rmse)
#
# plt.plot(test)
# plt.plot(predictions, color='red')
# plt.title('RMSE: %.3f' % rmse)
# plt.show()

for data in dataset:
    util.train_test(data, True)