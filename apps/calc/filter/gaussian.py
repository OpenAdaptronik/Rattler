import numpy as np
from scipy.signal import gaussian
from scipy.ndimage import filters



def gaussian_filter(data, index, gauss_std=2):
    '''
    The gaussian filter with the default number of points in the output window (Equal the points of the input)
    :param data: The data array (Pandas Data Frame)
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
    daten = np.asarray(data.iloc[:, index], dtype=np.result_type(float, np.ravel(data.iloc[:, index])[0]))
    b = gaussian(len(data.iloc[:,0]), gauss_std)
    return filters.convolve1d(daten, b / b.sum())


def gaussian_filter(data, index, gauss_M=50, gauss_std=2):
    '''
    The gaussian filter with the customizable number of points in the output window
    :param data: The data array (Pandas Data Frame)
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
    daten = np.asarray(data.iloc[:, index], dtype=np.result_type(float, np.ravel(data.iloc[:, index])[0]))
    b = gaussian(gauss_M, gauss_std)
    return filters.convolve1d(daten, b / b.sum())