import pandas as pd
import numpy as np
import scipy as sci





# Header = None -> ignoriert
daten = pd.read_csv('CSV_files/multidata_equal_/single_multidata_equal_Time_data.csv')
daten2 = pd.read_csv('CSV_files/multidata_equal_/none_multidata_equal_Time_data.csv')

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



print(header_Format(daten2))
print(daten.iloc[:,1])

