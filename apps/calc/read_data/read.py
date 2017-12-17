import pandas as pd
import numpy as np
from calculus import get_delta
from collections import Counter

class Measurement(object):
    colNames_User = []
    colUnits_User = []
    data = pd.DataFrame

    def __init__(self, raw):
        self.data = self.get_column_names(self.header_format(raw))

    def new_resample_data(self,time_index=0):
        '''

        :param time_index:
        :return:
        '''
        cnt=Counter(get_delta(self.data,time_index,4))
        N_new = int(round((self.data.iloc[:,0].iloc[-1]-self.data.iloc[:,0].iloc[0])/cnt.most_common(1)[0][0]))
        print('N_new: ',N_new)
        m, n = (len(self.data.iloc[:,0]), N_new)
        T = 1. / n
        A = np.zeros((m, n))

        production_data = {}  # Create dict with the resampled Data

        for i in range(0,len(self.data.columns)):
            if i == time_index:
                production_data[self.data.keys()[i]] = np.linspace(self.data.iloc[:, i].iloc[0], self.data.iloc[:, i].iloc[-1], N_new)
            else:
                for j in range(0, m):
                    A[j, :] = np.sinc((self.data.iloc[:,i].iloc[j] - N_new) / T)
                production_data[self.data.keys()[i]] = np.linalg.lstsq(A, self.data.iloc[:,time_index])[0]

        self.data = pd.DataFrame(production_data, columns=self.data.keys())  # Generate new DataFrame from new Data
        print(self.data)

    def header_format(self,data):
        '''
        This method rearranges the data rows such that
        either the header row of the DataFrame is empty, it the input file had no header
        or filled with the header data if the input data had a head

        :param data: a Pandas DataFrame of Data
        :return: print a Data Preview of the Data
        :return: The header-normalized DataFrame
        '''
        # Preview Daten50
        print('Daten wurden erfolgreich eingelesen: \n\n', data.head())

        headerColumns = data.columns.values

        #Check weather the Data start with Numbers (--> No Head) or something else
        try:
            float(headerColumns[0])
        except:
            return data #Has Head

        #Fill Head with its Index
        data.loc[-1] = headerColumns
        data.index = data.index + 1
        data = data.sort_index()
        data.columns = range(len(headerColumns)-1)

        return data

    # Fragt den Nutzer nach den Bezeichnern der Spalte und in welcher Einheit diese Daten gemessen wurde und fügt die Einheiten an idx = 0 ein
    def get_column_names(self,data):
        '''
        Die Methode fragt den Nutzer nach den Bezeichnern der Spalte ab und in welcher Einheit diese Daten gemessen wurden.
        Die Bezeichner/Namen werden in den Head geschrieben und die Einheiten werden in die Zeile mit den Listenindex
        idx = 0 geschrieben. Somit fangen die Werte erst ab Index 1 an, dies muss bei Berechnungen beachtet werden.

        Warning: Since this method uses the public class Variables colNames_User, colUnits_User -use this Function only once
        per Instance!!!

        :param data: List mit
        :return: Datenliste mit Bezeichnern im Head und Einheiten in Zeile mit Index 0
        '''
        i = 0
        for value in list(data.head()):
            i += 1
            # Instance of Numpy.Int64 because of the fact that this is the standard type of an pandas Dataframe
            if isinstance(value, np.int64):
                # @TODO: Frontend, verhindert leere Eingabe
                self.colNames_User.append(input("Bitte geben Sie den Namen der " + str(i) + " Spalte ein:"))
            else:
                # @TODO: Frontend, verhindert leere Eingabe
                self.colNames_User.append(input('Wie möchten sie die Spalte ' + value + ' bennen? '))
        i = -1
        for value in list(data.head()):
            i += 1
            # @TODO: Frontend, Dropdown Liste
            self.colUnits_User.append(input('Bitte geben Sie die Einheit der Spalte ' + self.colNames_User[i] + ' ein: '))

        data.columns = self.colNames_User
        return data