from scipy.signal import butter,filtfilt
from calculus import get_delta


def butterworth_band_filter(data, data_index, time_index=0, order=4, lowcut = None, highcut = None):
    '''
    Filters high and lowpass
    :param data: The data array
    :param data_index: The index of interest for the data
    :param time_index: the index of the sampling time
    :param order: The order of the butter filter.
    :param lowcut: The low frequency cutoff, default 10% of the input frequency
    :param highcut: The high frequency cutoff, default 90% of the input frequency
    :return: the filtered data sequence

    Example:
    import matplotlib.pyplot as plt
    def butterworth_example(data):
        plt.figure
        plt.plot(data.iloc[:, 0], data.iloc[:, 1], 'b', alpha=0.75)
        plt.plot(data.iloc[:, 0], butterworth_band_filter(data, 1,), 'g')
        plt.legend(('noisy signal', 'high_butterworth', 'low_butterworth' , 'band_butterworth'), loc='best')
        plt.grid(True)
        plt.show()
    '''
    fs = 1/get_average_delta(data,time_index)
    nyq = 0.5 * fs
    
    #Default Values
    if lowcut ==None: 
        lowcut = 0.1*nyq
    if highcut == None: 
        highcut = 0.9*nyq
        
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order,[low,high] , btype='band', analog=False)
    return filtfilt(b, a, data.iloc[:, data_index])


def butterworth_filter(data, data_index, time_index=0, order=4, cofreq=None, mode='low'):
    '''
    Filters high or lowpass
    :param data: The data array
    :param data_index: The index of interest for the data
    :param time_index: the index of the sampling time
    :param order: The order of the butter filter.
    :param cofreq: The cuttoff frequency
    :param mode: disdinguish between 'high' for highpass and 'low' for lowpass
    :return: the filtered data sequence

    Example:
    import matplotlib.pyplot as plt
    def butterworth_example(data):
        plt.figure
        plt.plot(data.iloc[:, 0], data.iloc[:, 1], 'b', alpha=0.75)
        plt.plot(data.iloc[:, 0], butterworth_filter(data, 1, mode='high'), 'r')
        plt.plot(data.iloc[:, 0], butterworth_filter(data, 1, mode='low'), 'y')
        plt.legend(('noisy signal', 'high_butterworth', 'low_butterworth' , 'band_butterworth'), loc='best')
        plt.grid(True)
        plt.show()
    '''
    fs = 1 / get_average_delta(data, time_index)
    nyq = 0.5 * fs
    
    #Default Values
    if cofreq ==None: 
        if mode =='low':
            cofreq = nyq*0.9
        elif mode =='high':
            cofreq = nyq*0.1
        else:
            print('Wrong Input format: butterworth_filter : ',mode,cofreq)
        print('cofreq: ',cofreq)
    #@TODO: Nochmal überprüfen
    
    cut = cofreq / nyq
    b, a = butter(order, cut, btype=mode, analog=False)
    return filtfilt(b, a, data.iloc[:, data_index])



def get_average_delta(data,index):
    '''
    This function calculates the average difference between the values of one column
    :param data: the data array
    :param time_index: the index of the column of interest
    :return: average between all values in the column
    '''
    deltas = get_delta(data,index)
    return sum(deltas)/len(deltas)
