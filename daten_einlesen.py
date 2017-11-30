import pandas as pd
import numpy as np
import scipy as sci
from nose.util import tolist

daten = pd.read_csv('CSV_files/multidata_equal_/single_multidata_equal_Time_data.csv')
daten2 = pd.read_csv('CSV_files/multidata_equal_/none_multidata_equal_Time_data.csv')
#Preview Daten
print('Daten wurden erfolgreich eingelesen: \n\n',daten.head(10))


namen =[]
einheiten=[]
i=-1
for reihe in list(daten.head()):
    i+=1
    if isinstance(reihe, int):
        #@TODO: Frontend, verhindert leere Eingabe
        namen.append(input('Bitte geben Sie den Namen der '+i+1+' Spalte ein: '))
    else:
        # @TODO: Frontend, verhindert leere Eingabe
        namen.append(input('Wie möchten sie die Spalte '+reihe+ ' bennen? '))

i = -1
for reihe in list(daten.head()):
    i += 1
    # @TODO: Frontend, Dropdown Liste
    einheiten.append(input('Bitte geben Sie die Einheit der Spalte '+ namen[i]+ ' ein: '))

def get_number_starting_index(daten):
    i=0
    index = 0
    while not(isinstance(daten.loc([[i],[0]]), int)) and i<50:
        print(daten.loc([[i],[0]]),type(daten.loc([[i],[0]])))
        index = i
        i+=1
    return index


print(get_number_starting_index(daten))
data = np.array([])






