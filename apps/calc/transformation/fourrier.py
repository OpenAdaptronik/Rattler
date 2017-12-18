import scipy as sci

def fourier_transform(data, data_index):
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

    #@TODO: Parameter überprüfen
    fft = [abs(x) for x in sci.fft(data.iloc[:, data_index])]
    return fft[:round(len(fft)/2)]



