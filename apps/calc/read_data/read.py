import json
import numpy as np
from collections import Counter
import scipy as spi
from apps.calc.filter.calculus import get_delta




class Measurement(object):

    def __init__(self, raw,User_Names,Unit_Names,time=0):
        self.timeIndex = time
        self.data = np.array(json.loads(raw))
        self.colUnits_User = np.array(json.loads(Unit_Names))
        self.colNames_User = np.array(json.loads(User_Names))




    def get_data(self):
        return self.data

    def save_to_db(self):
        return True


    def resample_data(self,time_index=0,scale = 1.0):
        '''
        This function resamples the data it. Within this it uses the already most frequently used time interval.
        It can also upscale the datapoints (get more Datapoints)[scale > 1] or downscale the data [scale <1]

        If the scale is 1.0 it projects it only on a constant intervall
        e.g. if it is already constant, there will be no changes.

        the used function is described here: https://dsp.stackexchange.com/questions/8488/what-is-an-algorithm-to-re
        -sample-from-a-variable-rate-to-a-fixed-rate

        !Attention!: The data needs distinct column names!
        :param time_index: The index of the time column
        :param scale: The scale, the Data should be resampled
        '''
        begin = self.data.iloc[:, time_index].iloc[0]
        end = self.data.iloc[:, time_index].iloc[-1]
        cnt=Counter(get_delta(self.data,time_index,3))
        X_new = np.linspace(0.0, end , int(
            (round((end-begin) / cnt.most_common(1)[0][0])) * scale))

        production_data = {}  # Create dict with the resampled Data


        for i in range(0,len(self.data.columns)):
            if i == time_index:
                production_data[self.data.keys()[i]] = X_new
            else:
                s = spi.splrep(self.data.iloc[:, time_index],self.data.iloc[:,i])
                production_data[self.data.keys()[i]] = spi.splev(X_new,s)

        self.data = np.array(production_data, columns=self.data.keys())


    def header_format(self,data):
        '''
        This method rearranges the data rows such that
        either the header row of the DataFrame is empty, it the input file had no header
        or filled with the header data if the input data had a head

        :param data: a Pandas DataFrame of Data
        :return: print a Data Preview of the Data
        :return: The header-normalized DataFrame
        '''
        # Preview Daten
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
        data.columns = range(len(headerColumns))

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
