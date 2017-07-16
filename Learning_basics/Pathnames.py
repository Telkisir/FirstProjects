# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 16:39:17 2017

@author: Telkisir
"""
import pickle, fnmatch, re, os
import pandas as pd
import numpy as np

def getFileName():
    strKassenbuch = 'Bankzahlungen.csv'
    path =r'C:\Users\Telkisir\Documents\Kassenbuch'
    fileBank = 'TotalData_.p'
    return strKassenbuch, path, fileBank

def getDataPyth():
    strKassenbuch, path, fileBank = getFileName()
    pDic = fnmatch.filter(os.listdir(path),'*.p')
    dateRegex = re.compile(r'(\d{8})\.p')
    localPlace =  0
    for i in range(0,len(pDic)):
        if re.search(dateRegex, pDic[i]) != None:
            #lastdate = lastdate.append(re.search(re.compile(r'(\d{8})'), pDic[i]))
            temp =int(re.search(re.compile(r'(\d{8})'), pDic[i]).group())
            if temp > localPlace:
                localPlace = temp    
    df = pickle.load(open(os.path.join(path, 'TotalData_'+str(localPlace)+'.p'), 'rb'))
    return df




def FindID():
    #Finde einträge nach Angaben : Wert und columns Name
    #mit ID entsprechender Eintrag laden
    # ändern oder löschen
    print ('Nothing so fare')

def FindDuplicates():
    #Jahreszahl oder Monat oder selben Tag werden gedropt
    #Storgaeangabe schöner machen, derzeit findungs doppelt
    #temp drop unschön, da bei länge != 2 Fehler
    #Code derbe langsam, blacklist verwenden
    df = getDataPyth()
    storage = pd.DataFrame()
    #show dupblicates and drop them if wished
    delDf = df.drop( df.drop_duplicates().index) #funktioniert scheinbar mit dem Jahr nicht!
    df.drop_duplicates(inplace = True)
    blacklist = np.array(0) #soll doppelfindung verhindern
    
    '''
    1. suche mir Dopplungen mittels subset of dropduplicates für Zeilen Art, Oberstruktur, Betrag
    2. Vergleiche diese duplicate noch mit Datum
    '''
    duplies = df.drop(df.drop_duplicates(keep= False, subset=['Zahlungsart', 'Betrag', 'Oberstruktur','Verwendungszweck']).index)
    whitelist = ['Umbuchung  ', 'Miete Haendelstrasse 21 in  Kohlscheid  ',
       'Finanzierung A  ', 'Hochzeit  ',
       'Versicherungsnr. 072764358 Beitrag  Krankenversicherung  ',
       'Aufladung bei geringem Guthaben fue  r Ihr Prepaid-Konto 4915776822342-9  673. BLAU.DE SAGT DANKE  ',]
    listVerwendung = duplies.Verwendungszweck.unique()
    for indVer in listVerwendung:
        if not(indVer in whitelist):
            temp = df.loc[df.Verwendungszweck == indVer]
            storage = storage.append(temp)
            #TODO duplies funktioniert irgendwie nicht? Siehe Betrag 25.6 also duplicate die gar keine sind
            # Betrag scheint nicht zu funktionieren
            # Weitermachen, wenn 2. Bildschirm vorhanden
            '''
            for j in temp.index:
                if j != temp.index[0]:
                    
                    if df.loc[j, 'Buchung'] == df.loc[i, 'Buchung']:
                        print ('Doppelbuchung bei Index %i?'%j)
                    else:
                        deltaDays = abs(df.loc[j,'Buchung'] - df.loc[i, 'Buchung']).days
                        if np.isclose(deltaDays, 365, atol = 3) or (np.isclose(deltaDays, 30, atol = 2)):
                            if df.loc[j,'Buchung'] < df.loc[i, 'Buchung']:
                                delDf = delDf.append(df.loc[j])
                                df.drop(j, inplace = True)
                                temp.drop([i,j], inplace = True)
                            else:
                                delDf = delDf.append(df.loc[i])
                                df.drop(i, inplace = True)
                                temp.drop([i,j], inplace = True)
                            print ('Jahresfelher bei Index %i?'%j)
                    
                storage =  storage.append(temp)
            '''
        
            
            
    for i in df.index:#df.index:
        temp = df.loc[(test.Zahlungsart == 'BAR')&(df.Betrag == df.loc[i, 'Betrag'])& (df.Verwendungszweck == df.loc[i, 'Verwendungszweck'])]        
        blacklist = np.append(blacklist, temp.index) # späer doppelienträge löschen
        if len(temp)>1:
            for j in temp.index:
                if j != temp.index[0]:
                    if df.loc[j, 'Buchung'] == df.loc[i, 'Buchung']:
                        print ('Doppelbuchung bei Index %i?'%j)
                    else:
                        deltaDays = abs(df.loc[j,'Buchung'] - df.loc[i, 'Buchung']).days
                        if np.isclose(deltaDays, 365, atol = 3) or (np.isclose(deltaDays, 30, atol = 2)):
                            if df.loc[j,'Buchung'] < df.loc[i, 'Buchung']:
                                delDf = delDf.append(df.loc[j])
                                df.drop(j, inplace = True)
                                temp.drop([i,j], inplace = True)
                            else:
                                delDf = delDf.append(df.loc[i])
                                df.drop(i, inplace = True)
                                temp.drop([i,j], inplace = True)
                            print ('Jahresfelher bei Index %i?'%j)
                
            storage =  storage.append(temp)



                
    return storage, delDf

def CheckEntries(df_test):
    #Vergleiche ob Einträge doppelt mit Datum oder Bank/Bar
    listChecker = pd.DataFrame(index = np.arange(0, 0), columns = ['Wert', 'ID1', 'ID2']).astype(float)
    for i in range(0, len(df_test)):
        for j in range(i+1, len(df_test)):
            if df.Betrag.iloc[j] == df.Betrag.iloc[i]:
                listChecker.loc[0] = df.Betrag.iloc[0,i]
                print('gefunden:', df.Betrag.iloc[i], i, j)
    print('Übertragung nicht implemtieiert')


def getTimeStamp():
    '''import time
    lt = time.localtime()
    jahr, monat, tag = lt[:3]
    monat = str('%02i' % monat )
    stimestamp = str(jahr)+monat+str(tag)'''
    import datetime
   # datetime.datetime.today()
    return datetime.datetime.today().date()

def dumpData(df):
    strKassenbuch, path, fileBank = getFileName()
    tdate = getTimeStamp() #format date
    pickle.dump(df,open(os.path.join(path, 'TotalData_%s%s%s.p'%(tdate.year,tdate.strftime('%m'), tdate.strftime('%d'))), "wb"))