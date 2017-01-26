#!/usr/bin/python
"""
Created on Mon Jan 23 21:05:39 2017

@author: Telkisir
"""

#GUI 
#Vorrangig zum eintragen von Barausgaben
#spätere Optionen: Bankdaten aktualisieren
#Fit Funktion ansteuern

import pickle, re, fnmatch, os, tkinter as tk__
import numpy as np
from Pathnames import getFileName






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


def readInValue():
    value =VF1.get()
    da =VF2.get()
    oName =VF3.get()
    sDesc =VF4.get()
    sPerson =VF5.get()
    check = DAU(value, da, oName, sDesc, sPerson)
    if check == True:
        df =savetoBase(value, da, oName, sDesc, sPerson)
        return df

def savetoBase(value, datum, oName, desc, person):
    rowmax = len(df)
    df.loc[rowmax+1] = np.nan
    df.loc[rowmax+1, df.columns[0]] = datum
    df.loc[rowmax+1, 'Oberstruktur'] = oName
    df.loc[rowmax+1, 'Verwendungszweck'] = desc
    df.loc[rowmax+1, 'Betrag'] = value
    df.loc[rowmax+1, 'Zahlungsart'] = 'BAR'                
    df.loc[rowmax+1, df.columns[1]] = person     
    print ('Eintrag eingetragen')
    return df

def DAU(value, da, oName, sDesc, sPerson):
    while True:
        try:
            float(value), str(oName), str(sDesc), str(sPerson)
            OK = True
            break    
        except ValueError:
            print ('Eingabe nicht korrekt, bitte prüfen.')
            OK = False
            break            
    return OK

def saveIt():
    strKassenbuch, path, fileBank = getFileName()
    import time
    lt = time.localtime()
    jahr, monat, tag = lt[:3]
    monat = str('%02i' % monat )
    pickle.dump(df,open(os.path.join(path, 'TotalData_'+str(jahr)+monat+str(tag)+'.p'), "wb"))
    print ('Saved')
    
ro = tk__.Tk()
df = getDataPyth()

#Layout
ro.geometry("200x200")
x1 = 5
x2 = 60
B = tk__.Button(ro, text ="Betrag einlesen", command = readInValue)
B.place(x=100,y=160)
#Save
B2 = tk__.Button(ro, text ="Save", command = saveIt)
B2.place(x=10,y=160)

#Betrag  
L1 = tk__.Label(ro, text='Betrag:')
VF1 = tk__.Entry(ro, bd = 5) #Value Field
L1.place(x = x1, y= 40)
VF1.place(x =x2, y= 40)
#Datum
L2 = tk__.Label(ro, text='Datum:')
VF2 = tk__.Entry(ro, bd = 5) #Value Field
L2.place(x =x1, y= 60)
VF2.place(x =x2, y= 60)
#Verwendungszweck
L3 = tk__.Label(ro, text='Zweck:')
VF3 = tk__.Entry(ro, bd = 5) #Value Field
L3.place(x =x1, y= 80)
VF3.place(x =x2, y= 80)
#Genaue Beschreibung
L4 = tk__.Label(ro, text='Beschreibung:')
VF4 = tk__.Entry(ro, bd = 5) #Value Field
L4.place(x =x1, y= 100)
VF4.place(x =x2, y= 100)
#Genaue Beschreibung
L5 = tk__.Label(ro, text='Person:')
VF5 = tk__.Entry(ro, bd = 5) #Value Field
L5.place(x =x1, y= 120)
VF5.place(x =x2, y= 120)

ro.mainloop()


