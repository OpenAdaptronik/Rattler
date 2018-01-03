from scipy import interpolate
import json
import numpy as np
from collections import Counter
from apps.calc.filter.calculus import get_delta,get_average_delta



class Measurement(object):
    def __init__(self, raw, Column_Names, Unit_Names, time=0):
        self.timeIndex = int(time)
        self.data = np.array(json.loads(raw))
        self.colUnits = np.array(json.loads(Unit_Names))
        self.colNames = np.array(json.loads(Column_Names))



    def save_to_db(self):
        return True



    def resample_data(self,scale = 1.0):
        '''
        This function resamples the data it.colNames_User Within this it uses the already most frequently used time interval.
        It can also upscale the datapoints (get more Datapoints)[scale > 1] or downscale the data [scale <1]

        If the scale is 1.0 it projects it only on a constant intervall
        e.g. if it is already constant, there will be no changes.

        the used function is described here: https://dsp.stackexchange.com/questions/8488/what-is-an-algorithm-to-re
        -sample-from-a-variable-rate-to-a-fixed-rate
        /process/
        !Attention!: The data needs distinct column names!
        :param time_index: The index of the time column
        :param scale: The scale, the Data should be resampled
        '''
        begin = np.float64(self.data[self.timeIndex,0])
        end = np.float64(self.data[self.timeIndex,-1])
        cnt=Counter(get_delta(self.data,self.timeIndex,3))
        X_new = np.linspace(0.0, end , int(
            (round((end-begin) / cnt.most_common(1)[0][0])) * scale))


        for i in range(0,self.data.ndim):
            if i == self.timeIndex:
                self.data[i] = X_new
            else:
                s = interpolate.splrep(self.data[self.timeIndex],self.data[i])
                self.data[i] = interpolate.splev(X_new,s)





    def gaussian_filter(self, index, gauss_std=2):
        '''
        The gaussian filter with the default number of points in the output window (Equal the points of the input)
        :param index: The index of interest for the data
        :param gauss_std: The standard deviation, sigma.
        :return: The filtered Data

        Example:
        import matplotlib.pyplot as plt
        def gaussian_example(data):
            plt.figure
            plt.plot(data.iloc[:, 0], data.iloc[:, 1], 'b', alpha=0.75)
            plt.plot(data.iloc[:, 0], gaussian_filter(data, 1), 'r')
            plt.legend(('noisy signal', 'Gauß'), loc='best')
            plt.grid(True)
            plt.show()
        '''
        daten = np.asarray(self.data[index], dtype=np.result_type(float, np.ravel(self.data[index])[0]))
        b = signal.gaussian(len(self.data[0]), gauss_std)
        self.data[index] = signal.filters.convolve1d(daten, b / b.sum())



    def gaussian_filter(self, index, gauss_M=50, gauss_std=2):
        '''
        The gaussian filter with the customizable number of points in the output window
        :param index: The index of interest for the data
        :param gauss_M: Number of points in the output window of the gaussian Function.
        If zero or less, an empty array is returned.
        :param gauss_std: The standard deviation, sigma.
        :return: The filtered Data

        Example:
        import matplotlib.pyplot as plt
        def gaussian_example(data):
            plt.figure
            plt.plot(data.iloc[:, 0], data.iloc[:, 1], 'b', alpha=0.75)
            plt.plot(data.iloc[:, 0], gaussian_filter(data, 1, 100), 'r')
            plt.legend(('noisy signal', 'Gauß'), loc='best')
            plt.grid(True)
            plt.show()
        '''
        daten = np.asarray(self.data[index], dtype=np.result_type(float, np.ravel(self.data[index])[0]))
        b = signal.gaussian(gauss_M, gauss_std)
        self.data[index] = signal.filters.convolve1d(daten, b / b.sum())


    def butterworth_band_filter(self,data_index, order=4, lowcut=None, highcut=None):
        '''
        Filters high and lowpass
        :param data: The data array
        :param data_index: The index of interest for the data
        :param ti   me_index: the index of the sampling time
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
        fs = 1 / get_average_delta(self.data, self.timeIndex)
        nyq = 0.5 * fs

        # Default Values
        if lowcut == None:
            lowcut = 0.1 * nyq
        if highcut == None:
            highcut = 0.9 * nyq

        low = lowcut / nyq
        high = highcut / nyq
        b, a = signal.butter(order, [low, high], btype='band', analog=False)
        return signal.filtfilt(b, a, self.data.iloc[:, data_index])


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

    # Default Values
    if cofreq == None:
        if mode == 'low':
            cofreq = nyq * 0.9
        elif mode == 'high':
            cofreq = nyq * 0.1
        else:
            print('Wrong Input format: butterworth_filter : ', mode, cofreq)
        print('cofreq: ', cofreq)
    # @TODO: Nochmal korrektheit überprüfen

    cut = cofreq / nyq
    b, a = signal.butter(order, cut, btype=mode, analog=False)
    return signal.filtfilt(b, a, data.iloc[:, data_index])




