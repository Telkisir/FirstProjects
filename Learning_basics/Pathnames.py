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
    path = os.path.join(os.getcwd(),'Data')
    fileBank = 'TotalData_.p'
    return strKassenbuch, path, fileBank

def getDataPyth():
    # Suche mir die aktuellste Datei
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
    df = df.astype({'Betrag': np.float, 'Saldo':np.float})
    return df




def FindID():
    #Finde einträge nach Angaben : Wert und columns Name
    #mit ID entsprechender Eintrag laden
    # ändern oder löschen
    print ('Nothing so fare')

def FindDuplicates():
    #Jahreszahl oder Monat oder selben Tag werden gedropt
    # Eine Whitlist nimmt regelmäßige Zahlung im Vorfeld raus
    print ('Duplicate und Einträge mit falschem Tag werden entfernt')
    df = getDataPyth()
    delDf = df.drop( df.drop_duplicates().index) #funktioniert scheinbar mit dem Jahr nicht!
    df.drop_duplicates(inplace = True)
    #Delete BAR duoubles
    duplies = df.drop(df.drop_duplicates(keep= False, subset=['Buchung', 'Betrag', 'Oberstruktur','Verwendungszweck', 'Auftraggeber/Empfänger']).index)
    df.drop(duplies.loc[duplies.Zahlungsart=='BAR'].index, inplace= True)
    duplies = df.drop(df.drop_duplicates(keep= False, subset=['Zahlungsart', 'Betrag', 'Oberstruktur','Verwendungszweck', 'Auftraggeber/Empfänger']).index)
    whitelist = ['Umbuchung  ', 'Miete Haendelstrasse 21 in  Kohlscheid  ',
       'Finanzierung A  ', 'Hochzeit  ',
       'Versicherungsnr. 072764358 Beitrag  Krankenversicherung  ',
       'Aufladung bei geringem Guthaben fue  r Ihr Prepaid-Konto 4915776822342-9  673. BLAU.DE SAGT DANKE  ',]
    listVerwendung = duplies.Verwendungszweck.unique()
    for indVer in listVerwendung:
        if not(indVer in whitelist):
            temp = duplies.loc[duplies.Verwendungszweck == indVer]
            listValues = temp.Betrag.unique()
            for indVal in listValues: 
                temp_double = temp.loc[temp.Betrag == indVal]
                if len(temp_double) == 2: # Annahme nur zwei Einträge
                    if np.diff(temp_double.Buchung).astype('timedelta64[D]').astype(np.int)[0] in [28,29,30,31,32,365,364,366]:
                         if temp_double.Buchung.iloc[0] < temp_double.Buchung.iloc[1]:
                             delDf = delDf.append(temp_double.iloc[0])
                             df.drop(temp_double.iloc[0].name, inplace = True)
                         else:
                             delDf = delDf.append(temp_double.iloc[1])
                             df.drop(temp_double.iloc[1].name, inplace = True)
                    #else: Abweichung vermutlich kein Eingabefehler
                else:
                    print ('Für Betrag %f wurden beim Verwendungszweck %s mehr als zwei Dopplungen festgestellt',(indVal,indVer))

    dumpData(df)
    

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