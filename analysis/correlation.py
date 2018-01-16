import math

# input data
# used_medicine_quantity = [660435657, 767063356, 867632500, 818260329, 647045938, 468268392, 356511105, 382248686,
#                           583195899, 686006286, 733973048, 907851681]
# number_of_patients = [3792925, 3949827, 4512010, 4177475, 3433044, 2585334, 2139986, 2365389, 3570879, 3754740, 3788978,
#                       4274347]


def data_rage(x):
    return max(x) - min(x)


def quantile(x, p):
    p_index = int(p * len(x))
    return sorted(x)[p_index]


def interquantile(x):
    return quantile(x, 0.75) - quantile(x, 0.25)


def mean(x):
    return sum(x) / len(x)


def dot(v, w):
    return sum(v_i * w_i for v_i, w_i in zip(v, w))


def sum_of_squares(v):
    return dot(v, v)


def de_mean(x):
    x_bar = mean(x)
    return [x_i - x_bar for x_i in x]


def variance(x):
    n = len(x)
    deviations = de_mean(x)
    return sum_of_squares(deviations) / (n - 1)


def standard_deviation(x):
    return math.sqrt(variance(x))


def covariance(x, y):
    n = len(x)
    return dot(de_mean(x), de_mean(y)) / (n - 1)


def correlation(x, y):
    stdev_x = standard_deviation(x)
    stdev_y = standard_deviation(y)

    if stdev_x > 0 and stdev_y > 0:
        return covariance(x, y) / stdev_x / stdev_y
    else:
        return 0

#
# correlation_coefficient = correlation(used_medicine_quantity, number_of_patients)
# rounded_coefficient = round(correlation_coefficient, 2)
#
#
# print("Correlation Analysis Between Used Medicine Quantities And Number Of Patients")
# print("coefficient: ", rounded_coefficient)
