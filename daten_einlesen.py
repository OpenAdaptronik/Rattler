
import pandas as pd
import scipy as sci
from scipy.signal import butter, gaussian
import numpy as np
from scipy.ndimage import filters
import matplotlib.pyplot as plt


# Header = None -> ignoriert
head = pd.read_csv('CSV_files/multidata_equal_/single_time+multidata_equal_Time_data.csv', dtype=np.float_)
nohead = pd.read_csv('CSV_files/multidata_equal_/none_time+multidata_equal_Time_data.csv', dtype=np.float_)
masse_read = pd.read_csv('CSV_files/Massenschwinger/Simulation_3_Massenschwinger_Zeitdaten.txt')
phyphox = pd.read_excel('CSV_files/Phyphox/phyphox Erik 1.xls',dtype=np.float_)
# Preview Daten


colNames_User = []
colUnits_User = []


def headerFormat(data):
    # Preview Daten
    print('Daten wurden erfolgreich eingelesen: \n\n', data.head())

    headerColumns = data.columns.values
    hasHeader = False
    i=0
    try:
            float(headerColumns[0])
    except:
        hasHeader = True


    colHeader = []

    if(hasHeader):
        return data
    if(hasHeader == False):
        for values in headerColumns:
            colHeader.append(i)
            i+=1
        data.loc[-1] = headerColumns
        data.index = data.index+1
        data = data.sort_index()
        data.columns = colHeader

        i = 0
        while i < len(data.iloc[0]) :
            data.iloc[0][i] = np.float_(data.iloc[0][i])
            i+=1

        return data




# Fragt den Nutzer nach den Bezeichnern der Spalte und in welcher Einheit diese Daten gemessen wurde und fügt die Einheiten an idx = 0 ein
def get_column_names(data):
    '''
    Die Methode fragt den Nutzer nach den Bezeichnern der Spalte ab und in welcher Einheit diese Daten gemessen wurden.
    Die Bezeichner/Namen werden in den Head geschrieben und die Einheiten werden in die Zeile mit den Listenindex
    idx = 0 geschrieben. Somit fangen die Werte erst ab Index 1 an, dies muss bei Berechnungen beachtet werden.
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
    #data.loc[-1] = colUnits_User
    # @TODO Frontend Click liste der Titel
    #Index = int(input('Bitte geben Sie den Index des Namen von ' + str(colNames_User) + ' ein: '))
    #data.index = data.index+1
    #data.index = pd.to_datetime(data.index, unit=colUnits_User[Index])
   # data = data.sort_index()
    return data

#Highpass and lowpass filter
def butterworth_filter(data,data_index,time_index =0 ,order = 4, cofreq =1.5 , mode = 'low'):
    '''

    :param data: The data array
    :param data_index: The index of interest for the data
    :param time_index: the index of the sampling time
    :param order: The order of the butter filter.
    :param cofreq: The cuttoff frequency
    :param mode: disdinguish between 'high' for highpass and 'low' for lowpass
    :return: the filtered data sequence
    '''
    #@TODO: Parameter abklären
    #fs = 1/get_interval(data,time_index)
    fs = 10
    b, a = butter(order, cofreq/(fs*0.5),btype=mode, analog=False)
    return sci.signal.filtfilt(b,a,data.iloc[:,data_index])

#Example
def butterworth_example(data):
    plt.figure
    plt.plot(data.iloc[:, 0], data.iloc[:, 1], 'b', alpha=0.75)
    plt.plot(data.iloc[:, 0], butterworth_filter(data,1,mode='high'), 'r')
    plt.legend(('noisy signal','butterworth'), loc='best')
    plt.grid(True)
    plt.show()


#@TODO: Standartwerte mit Frauenhofer abklären
def gaussian_filter(data, index, gauss_M = 50, gauss_std = 2):
    '''
    :param data: The data array
    :param index: The index of interest for the data
    :param gauss_M: Number of points in the output window of the gaussian Function.
    If zero or less, an empty array is returned.
    :param gauss_std: The standard deviation, sigma.
    :return: The filtered Data
    '''
    daten = np.asarray(data.iloc[:,index], dtype=np.result_type(float, np.ravel(data.iloc[:,index])[0]))
    b = gaussian(gauss_M, gauss_std)
    return filters.convolve1d(daten, b/b.sum())



def resample_data(data):
    '''
    This function takes the data as pandas dataFrame and resamples it to a constant intervall with the same
    number of samples in the resulting data. The Values get rearreanged but not interpolated
    :param data: pandas DataFrame
    :return: resampled DataFrame
    '''
    df =pd.DataFrame(sci.signal.resample(data, len(data.iloc[:,0])),dtype=np.float_)
    df.columns = data.columns
    return df

def get_interval(data,time_index=0):
    '''
    This function calculates the average interval between the measurements
    :param data: the data array
    :param time_index: the index of the time column
    :return: the average distance in the time column[1:]
    '''
    res=[]
    for t1,t2 in zip(data.iloc[:,time_index][:-1],data.iloc[:,time_index][1:]):
        res.append(t2-t1)
    return sum(res)/len(res)


#Example
def gaussian_example(data):
    plt.figure
    plt.plot(data.iloc[:, 0], data.iloc[:, 1], 'b', alpha=0.75)
    plt.plot(data.iloc[:, 0], gaussian_filter(data, 1, len(data.iloc[:, 1])), 'r')
    plt.legend(('noisy signal','Gauß'), loc='best')
    plt.grid(True)
    plt.show()

def fourier_transform(data, data_index):
    '''
    This Method Applies a fourier transformation on an data interval in the data
    :param data: the pandas DataFrame of the data
    :param data_index: The index of the data intervall of
    :return: the list of fourrier transformed values
    '''
    fft = [sci.sqrt(x.real**2 + x.imag**2) for x in sci.fft(data.iloc[:, data_index])] #sci.fft(data.iloc[:, data_index])
    return fft

def fourier_example(data):
    plt.figure
    plt.plot(data.iloc[:, 0], data.iloc[:, 1], 'b', alpha=0.75)
    plt.plot(data.iloc[:, 0], fourier_transform(data, 1), 'r')
    plt.legend(('noisy signal','fourier'), loc='best')
    plt.grid(True)
    plt.show()

def get_sinus():
    N = 512  # Sample count
    return pd.DataFrame([ [t, sci.sin(t)]for t in range(N)],dtype=np.float_)


# Normalize Data
#phyphox = resample_data(get_column_names(headerFormat(phyphox)))
#masse  = resample_data(get_column_names(headerFormat(masse_read)))
#sinus = get_sinus()


#Filter Data
#butterworth_example(phyphox)
#gaussian_example(phyphox)
#fourier_example(sinus)




# data.iloc[rows , columns ]     rows :=    [0] select idx 0      [1:] 1bis ende     [1:5] 1-5      [:,-1] last column

def getDelta(data,index):
    res = []
    for t1, t2 in zip(data.iloc[:, index][:-1], data.iloc[:, index][1:]):
        res.append(t2 - t1)

    return res

def numericalApprox(data,diff_Value1_Index,diff_Value2_Index):
    diff_Value = []
    for v1, t1 in zip(getDelta(data,diff_Value1_Index), getDelta(data,diff_Value2_Index)):
        diff_Value.append(v1/t1)

    return diff_Value

print(numericalApprox(masse_read,2,0))


