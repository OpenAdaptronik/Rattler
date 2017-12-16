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
        plt.plot(data.iloc[:, 0], data.iloc[:, 1], 'b', alpha=0.75)
        plt.plot(data.iloc[:, 0], fourier_transform(data, 1), 'r')
        plt.legend(('noisy signal', 'fourier'), loc='best')
        plt.grid(True)
        plt.show()
    '''
    fft = [sci.sqrt(x.real ** 2 + x.imag ** 2) for x in
           sci.fft(data.iloc[:, data_index])]
    return fft



