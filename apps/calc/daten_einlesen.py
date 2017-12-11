import pandas as pd
import scipy as sci
from scipy.signal import butter, gaussian
import numpy as np
from scipy.ndimage import filters
import matplotlib.pyplot as plt
#from apps.calc.tess import tess

# Header = None -> ignoriert
head = pd.read_csv('data_files/multidata_equal_/single_time+multidata_equal_Time_data.csv', dtype=np.float_)
nohead = pd.read_csv('data_files/multidata_equal_/none_time+multidata_equal_Time_data.csv', dtype=np.float_)
masse_read = pd.read_csv('data_files/massenschwinger/Simulation_3_Massenschwinger_Zeitdaten.txt')
phyphox = pd.read_excel('data_files/phyphox/phyphox Erik 2.xls', dtype=np.float_)

colNames_User = []
colUnits_User = []


def header_format(data):
    '''
    This method rearranges the data rows such that
    either the header row of the DataFrame is empty, it the input file had no header
    or filled with the header data if the input data had a head

    :param data: a Pandas DataFrame of Data
    :return: print a Data Preview of the Data
    :return: The header-normalized DataFrame
    '''
    # Preview Daten
    print('Daten wurden erfolgreich eingelesen: \n\n', data.head())

    headerColumns = data.columns.values

    #Check weather the Data start with Numbers (--> No Head) or something else
    try:
        float(headerColumns[0])
    except:
        return data #Has Head

    #Fill Head with its Index
    data.loc[-1] = headerColumns
    data.index = data.index + 1
    data = data.sort_index()
    data.columns = range(len(headerColumns)-1)

    return data



# Fragt den Nutzer nach den Bezeichnern der Spalte und in welcher Einheit diese Daten gemessen wurde und fügt die Einheiten an idx = 0 ein
def get_column_names(data):
    '''
    Die Methode fragt den Nutzer nach den Bezeichnern der Spalte ab und in welcher Einheit diese Daten gemessen wurden.
    Die Bezeichner/Namen werden in den Head geschrieben und die Einheiten werden in die Zeile mit den Listenindex
    idx = 0 geschrieben. Somit fangen die Werte erst ab Index 1 an, dies muss bei Berechnungen beachtet werden.

    Warning: Since this method uses the public class Variables colNames_User, colUnits_User -use this Function only once
    per Instance!!!

    :param data: List mit
    :return: Datenliste mit Bezeichnern im Head und Einheiten in Zeile mit Index 0
    '''
    i = 0
    for value in list(data.head()):
        i += 1
        # Instance of Numpy.Int64 because of the fact that this is the standard type of an pandas Dataframe
        if isinstance(value, np.int64):
            # @TODO: Frontend, verhindert leere Eingabe
            colNames_User.append(input("Bitte geben Sie den Namen der " + str(i) + " Spalte ein:"))
        else:
            # @TODO: Frontend, verhindert leere Eingabe
            colNames_User.append(input('Wie möchten sie die Spalte ' + value + ' bennen? '))
    i = -1
    for value in list(data.head()):
        i += 1
        # @TODO: Frontend, Dropdown Liste
        colUnits_User.append(input('Bitte geben Sie die Einheit der Spalte ' + colNames_User[i] + ' ein: '))

    data.columns = colNames_User
    return data


# Highpass and lowpass filter
def butterworth_filter(data, data_index, time_index=0, order=4, cofreq=1.5, mode='low'):
    '''

    :param data: The data array
    :param data_index: The index of interest for the data
    :param time_index: the index of the sampling time
    :param order: The order of the butter filter.
    :param cofreq: The cuttoff frequency
    :param mode: disdinguish between 'high' for highpass and 'low' for lowpass
    :return: the filtered data sequence
    '''
    # @TODO: Parameter abklären
    # fs = 1/get_interval(data,time_index)
    fs = 10
    b, a = butter(order, cofreq / (fs * 0.5), btype=mode, analog=False)
    return sci.signal.filtfilt(b, a, data.iloc[:, data_index])


# @TODO: Standartwerte mit Frauenhofer abklären
def gaussian_filter(data, index, gauss_M=50, gauss_std=2):
    '''
    :param data: The data array
    :param index: The index of interest for the data
    :param gauss_M: Number of points in the output window of the gaussian Function.
    If zero or less, an empty array is returned.
    :param gauss_std: The standard deviation, sigma.
    :return: The filtered Data
    '''
    daten = np.asarray(data.iloc[:, index], dtype=np.result_type(float, np.ravel(data.iloc[:, index])[0]))
    b = gaussian(gauss_M, gauss_std)
    return filters.convolve1d(daten, b / b.sum())


def resample_data(data):
    '''
    This function takes the data as pandas dataFrame and resamples it to a constant intervall with the same
    number of samples in the resulting data. The Values get rearreanged but not interpolated
    :param data: pandas DataFrame
    :return: resampled DataFrame
    '''
    df = pd.DataFrame(sci.signal.resample(data, len(data.iloc[:, 0])), dtype=np.float_)
    df.columns = data.columns
    return df


def get_average_delta(data, time_index=0):
    '''
    This function calculates the average interval between the measurements
    :param data: the data array
    :param time_index: the index of the time column
    :return: the average distance in the time column[1:]
    '''
    res = []
    for t1, t2 in zip(data.iloc[:, time_index][:-1], data.iloc[:, time_index][1:]):
        res.append(t2 - t1)
    return sum(res) / len(res)


def get_delta(data, index):
    '''
    This function calculates the average difference between the values of one column
    :param data: the data array
    :param time_index: the index of the column of interest
    :return: a list of distances between all values in the column
    '''
    res = []
    for t1, t2 in zip(data.iloc[:, index][:-1], data.iloc[:, index][1:]):
        res.append(t2 - t1)
    return res


def fourier_transform(data, data_index):
    '''
    This Method Applies a fourier transformation on an data interval in the data
    :param data: the pandas DataFrame of the data
    :param data_index: The index of the data intervall of
    :return: the list of fourrier transformed values
    '''
    fft = [sci.sqrt(x.real ** 2 + x.imag ** 2) for x in
           sci.fft(data.iloc[:, data_index])]
    return fft

def numerical_approx(data, diff_Value1_Index, diff_Value2_Index = 0):
    '''
    This method derives one Data Column by another
    Zeitwerte oder die anderen Werte ?
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

def fourier_example(data):
    plt.figure
    plt.plot(data.iloc[:, 0], data.iloc[:, 1], 'b', alpha=0.75)
    plt.plot(data.iloc[:, 0], fourier_transform(data, 1), 'r')
    plt.legend(('noisy signal', 'fourier'), loc='best')
    plt.grid(True)
    plt.show()

def gaussian_example(data):
    plt.figure
    plt.plot(data.iloc[:, 0], data.iloc[:, 1], 'b', alpha=0.75)
    plt.plot(data.iloc[:, 0], gaussian_filter(data, 1, len(data.iloc[:, 1])), 'r')
    plt.legend(('noisy signal', 'Gauß'), loc='best')
    plt.grid(True)
    plt.show()


def butterworth_example(data):
    plt.figure
    plt.plot(data.iloc[:, 0], data.iloc[:, 1], 'b', alpha=0.75)
    plt.plot(data.iloc[:, 0], butterworth_filter(data, 1, mode='high'), 'r')
    plt.legend(('noisy signal', 'butterworth'), loc='best')
    plt.grid(True)
    plt.show()

#Just to generate Test Sinus Function
def get_sinus():
    N = 512
    return pd.DataFrame([[t, sci.sin(t)] for t in range(N)], dtype=np.float_)


#-------- Normalize Data --------
phyphox = resample_data(get_column_names(header_format(phyphox)))
# masse  = resample_data(get_column_names(headerFormat(masse_read)))
sinus = get_sinus()
# acceleration = numerical_approx(masse_read, 2, 0)

#-------- Filter Data --------
butterworth_example(phyphox)
gaussian_example(phyphox)
fourier_example(sinus)


# @TODO: Tess import fixen
# @TODO: Welche Daten kommen denn in Tess rein?
#print(tess.tess(phyphox.iloc[:, 0], phyphox.iloc[:, 1], phyphox.iloc[:, 2]))




