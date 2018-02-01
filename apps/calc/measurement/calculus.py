import numpy as np
import json
import scipy as sci

def get_decimal_delta(data, index,decimals):
    '''
    This function calculates the difference between the values of one column
    :param data: the data array
    :param time_index: the index of the column of interest
    :param decimals: Number of decimal places to round to (default: 0).
    If decimals is negative, it specifies the number of positions to the left of the decimal point.
    :return: a list of distances between all values in the column
    '''
    res = []
    for t1, t2 in zip(data[:-1,int(index)], data[1:,int(index)]):
        res.append(np.around(np.float64(t2) - np.float64(t1),decimals))
    return np.array(res)

def get_delta(data, index):
    '''
    This function calculates the difference between the values of one column
    :param data: the data array
    :param time_index: the index of the column of interest
    :param decimals: Number of decimal places to round to (default: 0).
    If decimals is negative, it specifies the number of positions to the left of the decimal point.
    :return: a list of distances between all values in the column
    '''
    realsol = []
    i=1

    while i < len(data[0:,index]):

        intervall = data[i, index]   - data[i - 1,index]

        realsol.append(intervall)
        i += 1
    realsol = np.array(realsol)
    return realsol


def get_average_delta(data, index):
    '''
    This function calculates the average difference between the values of one column
    :param data: the data array
    :param time_index: the index of the column of interest
    :return: average between all values in the column
    '''
    deltas = get_decimal_delta(data, index, 7)
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
    diff_Value.append(np.float_(0.000))
    data = np.array(json.loads(data), dtype=np.float64)



    for v1, t1 in zip(get_delta(data, int(diff_Value1_Index)), get_delta(data, int(diff_Value2_Index))):
        diff_Value.append(v1 / t1)



    return np.asarray(diff_Value)

def trapez_for_each(data, index_x, index_y):
        """
        This method integrates the given Values with the Trapeziodal Rule
        :param index_x: index der X Achse
        :param index_y: index der Y Achse
        :return: integrated Values from x,y
        """
        i = 1
        sol = []


        data =np.array(json.loads(data),dtype=np.float64)


        #data =np.array(json.loads(data),dtype=np.float_)


        while i < len(data[:,index_x]):
            res = sci.trapz(data[0:i, index_y], data[0:i, index_x])
            res = np.float_(res)
            sol.append(res)
            i += 1
        i = 0
        realsol = []
        while i < len(sol):

            intervall = sol[i] - sol[i - 1]

            if i == 0:
                realsol.append(np.float_(0))

            realsol.append(intervall)
            i += 1
        realsol= np.array(realsol)



        return realsol

