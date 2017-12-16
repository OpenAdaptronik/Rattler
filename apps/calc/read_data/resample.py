import numpy as np
import pandas as pd

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

