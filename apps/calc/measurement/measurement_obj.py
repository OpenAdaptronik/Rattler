from scipy import interpolate, signal,ndimage
import scipy as sci
import json
import numpy as np
from collections import Counter
from apps.calc.measurement.calculus import get_average_delta,get_delta



class Measurement(object):
    def __init__(self, raw, Column_Names, Unit_Names, time=0):
        self.timeIndex = int(time)
        self.data = np.array(json.loads(raw), dtype=np.float64)
        self.colUnits = np.array(json.loads(Unit_Names))
        self.colNames = np.array(json.loads(Column_Names))
        self.log = '-'



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
        :param scale: The scale, the Data should be resampled
        '''
        self.log = 'resample'
        begin = np.float64(self.data[0,self.timeIndex])
        end = np.float64(self.data[-1,self.timeIndex])
        cnt=Counter(get_delta(self.data,self.timeIndex,3))
        X_new = np.linspace(begin, end , int(
            (round((end-begin) / cnt.most_common(1)[0][0])) * scale))

        new_data = []

        for i in range(0,len(self.data[0])):
            if i == self.timeIndex:
                new_data.append(np.array(X_new))
            else:
                s = interpolate.splrep(self.data[:,self.timeIndex],self.data[:,i])
                new_data.append(np.array(interpolate.splev(X_new,s)))


        self.data = np.asarray(new_data,dtype="float64").transpose()


    def fourier_transform(self):
        '''
        This Method Applies a fourier transformation on an data interval in the data
        :param data: the pandas DataFrame of the data
        :param data_index: The index of the data intervall of
        :return: the list of fourrier transformed values

        Example:
        import matplotlib.pyplot as plt
        def fourier_example(data):
            plt.figure
            n = len(data.iloc[:, 0])
            plt.plot(data.iloc[:round(n/2), 0], data.iloc[:round(n/2), 1], 'b', alpha=0.75)
            plt.plot(data.iloc[:round(n/2), 0], fourier_transform(data, 1), 'r')
            plt.legend(('noisy signal', 'fourier'), loc='best')
            plt.grid(True)
            plt.show()
        '''
        self.log = 'fourrier'
        new_data = []
        cut = int(len(self.data[:, 0]) / 2)
        for i in range(0,len(self.data[0])):
            if i == self.timeIndex:
                X_new = np.fft.fftfreq(len(self.data[:,i]), d=get_average_delta(self.data,i))[:cut]
                new_data.append(np.array(X_new))

            else:
                fft = [np.real(x) for x in sci.fft(self.data[:, i])]
                new_data.append(np.array(fft[:cut]))

        self.colUnits[self.timeIndex] = 'Hz'
        self.colNames[self.timeIndex] = 'Frequenz'
        self.data = np.asarray(new_data,dtype="float64").transpose()




    def gaussian_filter(self, index, gauss_std=2 , gauss_M=None):
        '''
        The gaussian filter with the default number of points in the output window (Equal the points of the input)
        :param index: The index of interest for the data
        :param gauss_std: The standard deviation, sigma.
        :return: The filtered Data

        Example:
        import matplotlib.pyplot as plt
        def gaussian_example(data):
            plt.figure
            plt.plot(data[0], data[1], 'b', alpha=0.75)
            plt.plot(data[0], gaussian_filter(data, 1), 'r')
            plt.legend(('noisy signal', 'Gauß'), loc='best')
            plt.grid(True)
            plt.show()
        '''
        self.log ='gauss'
        daten = np.asarray(self.data[:,index], dtype=np.float64)
        if gauss_M == None:
            b = signal.gaussian(len(self.data[:,0]), gauss_std)
        else:
            b = signal.gaussian(gauss_M, gauss_std)
        self.data[:,index] = ndimage.convolve1d(daten, b / b.sum())



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
        self.log= 'hoch und tief'
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
        self.data[:,data_index] = signal.filtfilt(b, a, np.float64(self.data[:,data_index]))


    def butterworth_filter(self, data_index, order=4, cofreq=None, mode='low'):
        '''
        Filters high or lowpass
        :param data_index: The index of interest for the data
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
        self.log ='hoch oder tief'
        fs = 1 / get_average_delta(self.data, self.timeIndex)
        nyq = 0.5 * fs

        # Default Values
        if cofreq == None:
            if mode == 'low':
                cofreq = nyq * 0.9
            elif mode == 'high':
                cofreq = nyq * 0.1
            else:
                print('Wrong Input format: butterworth_filter : ', mode, cofreq)

        cut = cofreq / nyq
        b, a = signal.butter(order, cut, btype=mode, analog=False)
        self.data[:,data_index] = signal.filtfilt(b, a, np.float64(self.data[:, data_index]))



    def trapez_for_each(self, index_x, index_y):
        """
        This method integrates the given Values with the Trapeziodal Rule
        :param index_x: index der X Achse
        :param index_y: index der Y Achse
        :return: integrated Values from x,y
        """
        i = 1
        sol = []

        while i < len(self.data[:,index_x]):
            res = sci.trapz(self.data[0:i, index_y], self.data[0:i, index_x])
            res = np.float_(res)
            sol.append(res)
            i += 1
        i = 1
        realsol = []
        while i < len(sol):

            intervall = sol[i] - sol[i - 1]

            if i == 1:
                realsol.append(np.float_(0))

            realsol.append(intervall)
            i += 1
        return np.asarray(realsol)



