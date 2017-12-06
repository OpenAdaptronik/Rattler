
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
# Preview Daten
print('Daten wurden erfolgreich eingelesen: \n\n', masse_read.head())

colNames_User = []
colUnits_User = []


def headerFormat(data):
    headerColumns = data.columns.values
    hasHeader = False
    i=0
    try:
            float(headerColumns[0])
    except:
        hasHeader = True

    if(hasHeader):
        print("hat header")
    else:
        print("hat kein header")

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


masse = get_column_names(headerFormat(masse_read))

#Highpass and lowpass filter
def butterworth_filter(data,index,fs=10,order = 4, cofreq =1.5 , mode = 'low'):
    '''

    :param data: The data array
    :param index: The index of interest for the data
    :param fs: the sampling rate
    :param order: The order of the butter filter.
    :param cofreq: The cuttoff frequency
    :param mode: disdinguish between 'high' for highpass and 'low' for lowpass
    :return: the filtered data sequence
    '''
    b, a = butter(order, cofreq/ (fs*0.5),btype=mode, analog=False)
    return sci.signal.filtfilt(b,a,data.iloc[:,index])

#Example
def butterworth_example():
    plt.figure
    plt.plot(masse.iloc[:, 0], butterworth_filter(masse,1))
    plt.plot(masse.iloc[:, 0], masse.iloc[:, 1], 'b', alpha=0.75)
    plt.legend(('noisy signal', 'butterworth'), loc='best')
    plt.grid(True)
    plt.show()


#@TODO: Standartwerte mit Frauenhofer abklären
def testGauss(data,index, gauss_M = 50,gauss_std = 2):
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



#@TODO: Noch nicht implementiert
def resample_data(data, time_index):
    print(data)
    print(sci.signal.resample(data, data.iloc[:,0]))
    #data.resample(interval, label='right').sum()

def get_interval(data,time_index):
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
def gaussian_example():
    plt.figure
    plt.plot(masse.iloc[:, 0], testGauss(masse,1,len(masse.iloc[:, 1])), 'b')
    plt.plot(masse.iloc[:, 0], masse.iloc[:, 1], 'b', alpha=0.75)
    plt.legend(('Gauß','noisy signal'), loc='best')
    plt.grid(True)
    plt.show()


resample_data(masse,0)
#butterworth_example()
#gaussian_example()


# data.iloc[rows , columns ]     rows :=    [0] select idx 0      [1:] 1bis ende     [1:5] 1-5      [:,-1] last column

