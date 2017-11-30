import pandas as pd
import numpy as np
import scipy as sci

header_found = False

# Header = None -> ignoriert
daten = pd.read_csv('CSV_files/multidata_equal_/single_multidata_equal_Time_data.csv')
daten2 = pd.read_csv('CSV_files/multidata_equal_/none_multidata_equal_Time_data.csv', header=None)

# Preview Daten
print('Daten wurden erfolgreich eingelesen: \n\n', daten.head(10))

colNames_User = []
colUnits_User = []


# Fragt den Nutzer nach den Bezeichnern der Spalte und in welcher Einheit diese Daten gemessen wurde und fügt die Einheiten an idx = 0 ein
def firstFormat(data):
    i = -1
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


daten = firstFormat(daten2)
print(daten)
