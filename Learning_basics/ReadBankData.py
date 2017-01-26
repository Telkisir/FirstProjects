# -*- coding: iso-8859-15 -*-
"""
Created on Tue Jan 10 14:06:17 2017

@author: K. Biß
Program should read in exportes Data from IngDiba for book keeping
"""


import fnmatch, os, re, pandas as pd
from Dictonary_Oberstruktur import getFilterBankVerw, getFilterBankAuftrag
import pickle
from Pathnames import getFileName



def CollectBankData( Status):
#Lese alle csv dateien ein...
    strKassenbuch, path, fileBank = getFileName()
    if Status == False: 
        df = pickle.load(open(os.path.join(path,fileBank ), 'rb'))
    else:       
        print ('Daten werden neu eingeladen...')
        csvDic = fnmatch.filter(os.listdir(path),'Umsatzanzeige_*.csv')
        for inum, ind in enumerate(csvDic):
            if inum == 0:
                df = subCollect(ind)
            else:
                df = df.append(subCollect(ind))   
        df = df.drop_duplicates()
        pickle.dump(df,open(os.path.join(path, fileBank), "wb"))
    
    print('Bankdaten sind geladen')
    return df

def subCollect(ind):
    df = pd.read_csv(os.path.join(path, ind), skiprows=  7, sep=';', header =0, encoding='iso-8859-15' ) # später 0 auf variabel
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
        df.iloc[:][colName] = pd.to_datetime(df.iloc[:][colName]).dt.date
    return df

def convCategories(df, listIndex):
    #Oberklassen-Klassifikation per Buchungstext
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
                                    print ('Eintrag bereits geändert in',df.at[index2,Kategorie] , 'ersetzt durch ', Begriff, ' in Zeile ', index2)
                                    df.at[index2,Kategorie] = Begriff                            #print (df.loc[index2][Kategorie], index2 , index1, df.iloc[index2][index1])                      
                    except TypeError:
                        # ('Kein Wert angegeben in Zeile ', index2 , index1)  # noch ändern  
                        df.ix[index2,index1] = "Eintrag fehlt"
    return df



########################################
#############..MAIN..###################
########################################

def initiateBank():
    print ('Bankdaten werden eingeladen...')
    df = CollectBankData(True)
    return df
#Eingabe von Kassenzetteln (GUI!!!)

#df = MergeBandWa(df)

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