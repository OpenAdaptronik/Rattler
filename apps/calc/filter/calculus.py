import numpy as np
import scipy as sp

def get_delta(data, index,decimals=0):
    '''
    This function calculates the difference between the values of one column
    :param data: the data array
    :param time_index: the index of the column of interest
    :param decimals: Number of decimal places to round to (default: 0).
    If decimals is negative, it specifies the number of positions to the left of the decimal point.
    :return: a list of distances between all values in the column
    '''
    res = []
    for t1, t2 in zip(data[:-1,index], data[1:,index]):
        res.append(np.around(np.float64(t2) - np.float64(t1),decimals))
    return res

def get_average_delta(data, index):
    '''
    This function calculates the average difference between the values of one column
    :param data: the data array
    :param time_index: the index of the column of interest
    :return: average between all values in the column
    '''
    deltas = get_delta(data, index, 7)
    return sum(deltas) / len(deltas)


def numerical_approx(data, diff_Value1_Index, diff_Value2_Index = 0):
    '''
    This method derives one Data Column by another
    Zeitwerte
    Example: d Speed / d Time = Acceleration
    :param data: the pandas DataFrame of the data
    :param diff_Value1_Index: Index of the Column to get the derivative of
    :param diff_Value2_Index: Index of the deriving Column (Usually the Time index)
    :return:
    '''
    diff_Value = []
    for v1, t1 in zip(get_delta(data, diff_Value1_Index), get_delta(data, diff_Value2_Index)):
        diff_Value.append(v1 / t1)
    return diff_Value


