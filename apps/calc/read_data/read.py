import pandas as pd
import numpy as np

colNames_User = []
colUnits_User = []


def header_format(data):
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
def get_column_names(data):
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
    return data