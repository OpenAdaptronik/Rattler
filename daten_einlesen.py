import pandas as pd
import numpy as np
import scipy as sci
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt





# Header = None -> ignoriert
daten = pd.read_csv('CSV_files/multidata_equal_/single_multidata_equal_Time_data.csv')
daten2 = pd.read_csv('CSV_files/multidata_equal_/none_multidata_equal_Time_data.csv', header=None)
masse = pd.read_csv('CSV_files/Massenschwinger/Simulation_3_Massenschwinger_Zeitdaten.txt')
# Preview Daten
#print('Daten wurden erfolgreich eingelesen: \n\n', daten2.head(10))

colNames_User = []
colUnits_User = []



def header_Format(data):
    """

    :param data: the dataframe of the actuall csv - file
    :return: dataframe with a header of
    """
    i = 0
    colHeader = []



    colValues = data.columns.values
    if isinstance(data.columns.values,str):
        return data
    else:
        for values in data.columns.values:
            colHeader.append(i)
            i += 1

        print(colValues)
        data.loc[-1] = colValues
        data.index = data.index+1
        data = data.sort_index()
        data.columns = colHeader

        return data





# Fragt den Nutzer nach den Bezeichnern der Spalte und in welcher Einheit diese Daten gemessen wurde und fügt die Einheiten an idx = 0 ein
def firstFormat(data):
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
    data.loc[-1] = colUnits_User
    data.index = data.index + 1
    data = data.sort_index()
    return data


daten = firstFormat(masse)

#lowpass filter
def lowpass_filter(data,n=8,Wn=0.120):
    b, a = sci.signal.butter(n, Wn)
    #b, a = sci.signal.butter(2, 0.01,'low')
    #b, a = sci.signal.ellip(25,4, 1, 120, 5)  # Filter to be applied.
    return sci.signal.filtfilt(a,b,daten,padlen=150)

#Example
def lowpass_example():
    plt.figure
    plt.plot(masse.iloc[:, 0][1:], lowpass_filter(masse.iloc[:, 1][1:]), 'r')
    plt.plot(masse.iloc[:, 0][1:], masse.iloc[:, 1][1:], 'b', alpha=0.75)
    plt.legend(('noisy signal', 'filtfilt'), loc='best')
    plt.grid(True)
    plt.show()

#Gauß Filter
def gaussian_filter(data,window_len=11,window='hanning'):

    if data.ndim != 1:
        print(ValueError, "smooth only accepts 1 dimension arrays.")

    if data.size < window_len:
        print(ValueError, "Input vector needs to be bigger than window size.")


    if window_len<3:
        return data


    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        print(ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")


    s=np.r_[data[window_len-1:0:-1],data,data[-2:-window_len-1:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')
    return y

#Example
def gaussian_example():
    print(masse.iloc[:,1][1:])
    print(gaussian_filter(masse.iloc[:,1][1:]))



#gaussian_example()
