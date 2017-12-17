import numpy as np
import pandas as pd

def f(x):
    t = np.pi * 2.0 * x
    return np.sin(t) + .5 * np.sin(14.0*t)




def resample_data(data,time_index=0, scale=1.0):
    '''
    This function takes the data as pandas dataFrame and resamples it by upscaling i [scale > 1]
    or downscaling it [scale <1] to a constant intervall. If the
    If the scale is 1.0 it projects it only on a constant intervall e.g. if it is alredy constant, there is no change.

    !Attention!: The data needs distinct column names!
    :param data: pandas DataFrame
    :param time_index: The index of the time column
    :param scale: The scale, the Data should be resampled
    :return: resampled DataFrame
    '''
    #@TODO: Validieren
    n = round(len(data.iloc[:, time_index]) * scale)# calculate new length of sample

    i=0
    production_data = {} #Create dict with the resampled Data
    while(i<len(data.columns)):
        if i == time_index:
            production_data[data.keys()[i]]=np.linspace(data.iloc[:,i].iloc[0], data.iloc[:,i].iloc[-1], n)
        else:
            production_data[data.keys()[i]] = np.interp(
            np.linspace(0.0, 1.0, n, endpoint=False),  # where to interpret
            np.linspace(0.0, 1.0, len(data.iloc[:, time_index]), endpoint=False),  # known positions
            data.iloc[:, i],  # known data points
            )
        i = i+1
    return pd.DataFrame(production_data, columns=data.keys()) #Generate new DataFrame from new Data



import numpy as np
import pylab as py

import scipy.interpolate as spi
import numpy.random as npr
import numpy.linalg as npl

npr.seed(0)

class Signal(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def plot(self, title):
        self._plot(title)
        py.plot(self.x, self.y ,'bo-')
        py.ylim([-1.8,1.8])
        py.plot(hires.x,hires.y, 'k-', alpha=.5)

    def _plot(self, title):
        py.grid()
        py.title(title)
        py.xlim([0.0,1.0])

    def sinc_resample(self, xnew):
        m,n = (len(self.x), len(xnew))
        T = 1./n
        A = np.zeros((m,n))

        for i in range(0,m):
            A[i,:] = np.sinc((self.x[i] - xnew)/T)

        return Signal(xnew, npl.lstsq(A,self.y)[0])

    def spline_resample(self, xnew):
        s = spi.splrep(self.x, self.y)
        return Signal(xnew, spi.splev(xnew, s))

class Error(Signal):

    def __init__(self, a, b):
        self.x = a.x
        self.y = np.abs(a.y - b.y)

    def plot(self, title):
        self._plot(title)
        py.plot(self.x, self.y, 'bo-')
        py.ylim([0.0,.5])

def grid(n): return np.linspace(0.0,1.0,n)
def sample(f, x): return Signal(x, f(x))

def random_offsets(n, amt=.5):
    return (amt/n) * (npr.random(n) - .5)

def jittered_grid(n, amt=.5):
    return np.sort(grid(n) + random_offsets(n,amt))


n = 30
m = n + 1

# Signals
even   = sample(f, np.r_[1:n+1] / float(n))
uneven = sample(f, jittered_grid(m))
hires  = sample(f, grid(10*n))

sinc   = uneven.sinc_resample(even.x)
spline = uneven.spline_resample(even.x)

sinc_err   = Error(sinc, even)
spline_err = Error(spline, even)

# Plot Labels
sn = lambda x,n: "%sly Sampled (%s points)" % (x,n)
r  = lambda x: "%s Reconstruction" % x
re = lambda x: "%s Error" % r(x)

plots = [
    [even,       sn("Even", n)],
    [uneven,     sn("Uneven", m)],
    [sinc,       r("Sinc")],
    [sinc_err,   re("Sinc")],
    [spline,     r("Cubic Spline")],
    [spline_err, re("Cubic Spline")]
]

for i in range(0,len(plots)):
    py.subplot(3, 2, i+1)
    p = plots[i]
    p[0].plot(p[1])
py.show()