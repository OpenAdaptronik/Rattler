import pandas as pd
import scipy as sci
import numpy as np





head = pd.read_csv('data_files/multidata_equal_/single_time+multidata_equal_Time_data.csv', dtype=np.float_)
nohead = pd.read_csv('data_files/multidata_equal_/none_time+multidata_equal_Time_data.csv', dtype=np.float_)
#print((daten["Force"]))



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




x=headerFormat(head)
print(type(x.iloc[0].iloc[4]))
x=x.iloc[2: , -1]
print(x)


