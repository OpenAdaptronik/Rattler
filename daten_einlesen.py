import pandas as pd
import numpy as np
import scipy as sci
from nose.util import tolist


header_found = False

#Header = None -> ignoriert
daten = pd.read_csv('CSV_files/multidata_equal_/single_multidata_equal_Time_data.csv')
daten2 = pd.read_csv('CSV_files/multidata_equal_/none_multidata_equal_Time_data.csv', header=None)
label = daten2.columns.values

print(label)

#Preview Daten
#print('Daten wurden erfolgreich eingelesen: \n\n',daten.head(10))





colNames_User =[]
colUnits_User =[]
i=-1
for reihe in list(daten.head()):
    i+=1
    if isinstance(reihe, int):
        #@TODO: Frontend, verhindert leere Eingabe
        colNames_User.append(input('Bitte geben Sie den Namen der '+i+1+' Spalte ein: '))
    else:
        # @TODO: Frontend, verhindert leere Eingabe
        colNames_User.append(input('Wie möchten sie die Spalte '+reihe+ ' bennen? '))

i = -1
for reihe in list(daten.head()):
    i += 1
    #@TODO: Frontend, Dropdown Liste
    colUnits_User.append(input('Bitte geben Sie die Einheit der Spalte '+ colNames_User[i]+ ' ein: '))

daten.columns = colNames_User

daten.loc[-1] = colUnits_User
daten.index = daten.index + 1
daten = daten.sort_index()

print(daten)








