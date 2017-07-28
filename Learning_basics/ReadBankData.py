# -*- coding: iso-8859-15 -*-
"""
Created on Tue Jan 10 14:06:17 2017

@author: K. Biß
Program should read in exportes Data from IngDiba for book keeping
"""
#To dO:
#Unterstruktur fehlen noch
#Überschreibungen nicht als print sondern in txt ablegen
'''
Aktuelle Arbeit:
    db drei fehlende Einträge löschen manuall neue Total 0126 anlegen
    fitl für Januar erweitern
    ...Untersektoren anlegen
    Index homogenisieren . duplicate funktioniert noch?
    update im test modus (filter anüpassen nicht abspeichern)
'''

import fnmatch, os, re, pandas as pd
from Dictonary_Oberstruktur import getFilterBankVerw, getFilterBankAuftrag, getColName
import pickle
from Pathnames import getFileName, getDataPyth, getTimeStamp, dumpData
import numpy as np



def CollectBankData( Status = False):
#Lese alle csv dateien ein...
    strKassenbuch, path, fileBank = getFileName()
    if Status == False: 
        df = getDataPyth()
    else:       
        print ('Daten werden neu eingeladen...')
        csvDic = fnmatch.filter(os.listdir(path),'Umsatzanzeige_*.csv')
        for inum, ind in enumerate(csvDic):
            if inum == 0:
                df = subCollect(ind, path)
            else:
                df = df.append(subCollect(ind, path))   
        df = sortDate(df)
        df = setHardList(df)
        #pickle.dump(df,open(os.path.join(path, fileBank), "wb"))
        dumpData(df)
        #tdate = getTimeStamp() #format date
        #pickle.dump(df,open(os.path.join(path, 'TotalData_%s%s%s.p'%(tdate.year,tdate.strftime('%m'), tdate.strftime('%d'))), "wb"))
    print('Bankdaten sind geladen')
    return df

def setHardList(df):
    path = os.path.join(os.getcwd(),'Data','Hardlist.xlsx' )
    df_hard = pd.read_excel(path)
    #df = getDataPyth()
    
    df = getColName(df)
    df_hard = getColName(df_hard)
    for ind in df_hard.index:
        df.loc[(df.BText == df_hard.loc[ind, 'BText'])   & 
              (df.Person == df_hard.loc[ind, 'Person']) &
              (df.Zweck == df_hard.loc[ind, 'Zweck']) & 
              (df.Betrag == df_hard.loc[ind, 'Betrag']) , 'Oberstruktur'] = df_hard.loc[ind, 'Oberstruktur']

    return df

def subCollect(ind, pathtoData):
    if int((ind.split('_'))[2].split('.csv')[0]) > 20170200:
        numrows = 6
    else:
        numrows = 7
    df = pd.read_csv(os.path.join(pathtoData, ind), skiprows=  numrows, sep=';', header =0, encoding='iso-8859-15' ) # später 0 auf variabel
    #df = pd.read_csv(os.path.join(path, csvDic[0]), skiprows=  7, sep=';', header =0, encoding='iso-8859-15' )
    #df['Buchung'] = pd.to_datetime(df['Buchung'], yearfirst = True, format='%d.%m.%Y').dt.date
    #df.loc[:,'Valuta'] = pd.to_datetime(df.loc[:,'Valuta']).dt.date
    df = convFloat(df, ['Saldo','Betrag']) # mache aus 2.500,00 --> 2500.00
    df = convDate(df,['Buchung','Valuta']) # mache aus String --> date
    df = df.drop(df.columns[[1,6,8]], axis=1) # lösche Währung und Valuta
    df = convCategories(df, [3,1] ) #3= Verwendungszweck , 1 =Empfänger
    List = df.loc[df['Oberstruktur'] =='KEINE'].index 
    #print (List)
    df.ix[List,6]='REST' 
    df['Zahlungsart'] = pd.Series('Bank', index=df.index)
    return df

def convFloat(df, column):
    for colName in column:
        tempSaldo = df.loc[:,[colName]]
        for index2 in range(0,len(tempSaldo)):
            conRegex = re.compile(r'\.(\d{3}\.)') # Solange beträg unter 1 Millionen ok
            tempSaldo.iloc[index2][colName] = tempSaldo.iloc[index2][colName].replace(',','.')
            tempSaldo.iloc[index2][colName] = conRegex.sub(r'\1' , tempSaldo.iloc[index2][colName] )
            #print (tempSaldo.iloc[index2]['Saldo'] )    
        df.iloc[:][colName] =  tempSaldo   
        df.iloc[:][colName] = pd.to_numeric(df.iloc[:][colName])
    return df

def convDate(df, column):
    for colName in column:
        df[colName] = pd.to_datetime(df[colName], yearfirst = True, format='%d.%m.%Y').dt.date
    return df

def convCategories(df, listIndex):
    #Oberklassen-Klassifikation per Buchungstext
    if 'Oberstruktur' in df.columns:
        print ('OK')    
    else:
        df['Oberstruktur'] = pd.Series('KEINE', index=df.index)
    df= searchReplace(df, listIndex, 'Oberstruktur')
    convRatioBank(df)    
    #Unterklassen-Klassifikation per Auftraggeber/Empfänger und Verwendungszweck    
    #rename Index
    
    return df

def convRatioBank(df):
    counter =0
    for index2 in range(0,len(df)):
        if df.at[index2,'Oberstruktur']=='KEINE':
            counter = counter +1
    print ((counter/len(df)*100) , '% noch offen')
    return (counter/len(df)*100)


def searchReplace(df, listIndex, Kategorie):
    changeList = []
    for index1 in listIndex:
        if index1 == 1:
            listRegex = getFilterBankAuftrag()
            print ('Detail durch empfanger')
        else:
            listRegex = getFilterBankVerw()
        for k, v in listRegex.items():
            Begriff = k
            Regex = v
            for index2 in range(0,len(df)):
                #print ('Hallo', df.ix[index2, index1]  )
                if Begriff == 'Einnahmen':
                    if df.iloc[index2]['Betrag']> 0:
                        df.at[index2,Kategorie] = Begriff
                else:
                    try:
                        if Regex.search(df.ix[index2, index1]) != None:
                            
                            if Begriff == 'Gina':
                                print('Reweeinkauf am:',df.iloc[index2][0],' fuer ',  df.iloc[index2][4], 'EUR' )
                            elif df.at[index2,Kategorie] =='KEINE':
                                df.at[index2,Kategorie] = Begriff
                            else:
                                if df.at[index2,Kategorie] != Begriff:                                     
                                    changeList = changeList.append('Eintrag bereits geändert in',df.at[index2,Kategorie] , 'ersetzt durch ', Begriff, ' in Zeile ', index2)
                                    print ('Eintrag bereits geändert in',df.at[index2,Kategorie] , 'ersetzt durch ', Begriff, ' in Zeile ', index2)
                                    df.at[index2,Kategorie] = Begriff                            #print (df.loc[index2][Kategorie], index2 , index1, df.iloc[index2][index1])                      
                    except TypeError:
                        # ('Kein Wert angegeben in Zeile ', index2 , index1)  # noch ändern  
                        df.ix[index2,index1] = "Eintrag fehlt"
        if len(changeList) > 0:
            pickle.dump(changeList,open(os.path.join('Hinweisprotokoll_'+getTimeStamp()+'.p'), "wb"))  
            print ('Hinweise ausgeschrieben')
    return df




########################################
#############..MAIN..###################
########################################

def initiateBank():
    print ('Bankdaten werden eingeladen...')
    df = CollectBankData(True)
    return df

def updateBank(test):
    df = getDataPyth()    
    strKassenbuch, path, fileBank = getFileName()    
    print ('Daten werden aktualisiert...')
    csvDic = fnmatch.filter(os.listdir(path),'Umsatzanzeige_*.csv')
    for inum, ind in enumerate(csvDic):
        df = df.append(subCollect(ind, path))   
    df = sortDate(df)
    
    if test == True:
        dumpData(df)
        #pickle.dump(df,open(os.path.join(path, 'TotalData_'+sTimeStamp+'.p'), "wb"))
        #tdate = getTimeStamp()
        #pickle.dump(df,open(os.path.join(path, 'TotalData_%s%s%s.p'%(tdate.year,tdate.month, tdate.day)), "wb"))
    print('Bankdaten sind aktualisiert')
    return df

def ResetRest(df, overwrite):  
    
    if overwrite == True:
        List = df.loc[df['Oberstruktur'] =='Rest'].index 
        df.ix[List,6]='Sonstige' 
    
    return  df.loc[df['Oberstruktur'] == 'REST']   

def sortDate(df):
    df = df.sort_values('Buchung', axis = 0)
    df = df.drop_duplicates()
    df = df.set_index(np.arange(0, len(df)))    
    return df
#Auswertung
#Monatsausgabe der Kategorien
#Abgleich von theoretisch zu erfasstem wert und fixen

# Jahresplanung und Projektionen




#Liste zur bestehenden dataframe hinzufügen

'''
Codes
#df2 = df.unstack()
#df3 = df.groupby(by='Buchung').sum()


#http://chrisalbon.com/python/pandas_dataframe_importing_csv.html      
#wb = openpyxl.load_workbook(csvFiles[0]) # nachher for schleife
#ws = wb.get_index(0)

#for rowloc in ws['A1':'C4']:
#    rowloc.find('Konto')
#    print (rowloc)       
 #df0  = pd.read_csv('Umsatzanzeige_5416578386_20170110.csv',  sep=";", encoding='iso-8859-15' )   

#
#http://pandas.pydata.org/pandas-docs/stable/indexing.html  
'''