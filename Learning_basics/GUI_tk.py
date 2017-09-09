#!/usr/bin/python
"""
Created on Mon Jan 23 21:05:39 2017

@author: Telkisir
"""

#GUI 
#Vorrangig zum eintragen von Barausgaben
#spätere Optionen: Bankdaten aktualisieren
#Fit Funktion ansteuern

import tkinter as tk__
import numpy as np
from Pathnames import getDataPyth, dumpData, FindDuplicates
from ReadBankData import UpdateBankData
import pandas as pd

def readInValue():
    #hier auch Gruppe neu setzen ne muss nicht da df gesetzt weird
    value =VFvalue.get()
    da =VFdate.get()
    oName =sGroup.get()
    sDesc =VFdesc.get()
    sPerson = sUser.get()
    check = DAU(value, da,  sDesc)
    if check == True:
        df =savetoBase(value, da, oName, sDesc, sPerson)
        clearArrays()
        #delID() Warum steht das hier?
        return df

def savetoBase(value, datum, oName, desc, person):
    df = getDataPyth()
    rowmax = len(df)
    if VFID.get() == '':
        valInd = rowmax +1
    else:
        valInd = float(VFID.get())
        print ('Wert wird ersetzt')
    df.loc[valInd] = np.nan
    #tdate = datetime.datetime.strptime(datum,"%d.%m.%Y").date()
    df.loc[valInd, df.columns[0]] = pd.to_datetime(datum, yearfirst = True, format='%d.%m.%Y').date()
    df.loc[valInd, 'Oberstruktur'] = oName
    df.loc[valInd, 'Zweck'] = str(desc)
    df.loc[valInd, 'Betrag'] = float(value)*-1
    df.loc[valInd, 'Zahlungsart'] = 'BAR'                
    df.loc[valInd, df.columns[1]] = person     
    print ('Eintrag eingetragen')
    dumpData(df)
    return df


def DAU(value, da, sDesc):
    #Prüft ob Daten dem vorgesehenem Format entsprechen
#    while True:
    try:
        float(value), str(sDesc), pd.to_datetime(da, yearfirst = True, format='%d.%m.%Y').date()
        if len(sDesc)< 8 :
            print('%s in Description too short. Please fill in more text'%sDesc)
            OK = False
        else:
            OK = True
        #break    
    except ValueError:
        try:
            pd.to_datetime(da, yearfirst = True, format='%d.%m.%Y').date()           
        except ValueError:
            print ('Datum nicht korrekt, bitte prüfen.')
        print ('Eingaben nicht korrekt, bitte prüfen.')
        OK = False
        #break            
    return OK

def findIt():
    if checkID():
        valID = int(VFID.get()) 
        clearArrays()
        VFID.insert(0,valID)
        VFdate.insert(0,df.loc[valID, df.columns[0]])
        VFvalue.insert(0, df.loc[valID, 'Betrag'])
        VFdesc.insert(0,df.loc[valID, 'Zweck']) 

 
def checkID():
    try:    
        if float(VFID.get()).is_integer():
            valID = int(VFID.get())
            try: 
                df.loc[valID, 'Betrag']
                return True
            except KeyError:
                print ('ID %i nicht bekannt'%valID)
                return  False
        else:
            print ('ID ist kein integer. Eingabe prüfen.')
            return  False 
    except ValueError:
        print ('Eingabe bei ID nicht korrekt, bitte prüfen.')
        return False
       
def printIt():    
    print ('Value is: %s'%sGroup.get())
    
def addSome():
    # Reset var and delete all old options
    sGroup.set('')
    dropGroup['menu'].delete(0, 'end')
    
    # Insert list of new options (tk._setit hooks them up to var)
    newchoice = np.append(lst1, VFgroup.get())
    
    for choice in newchoice:
        dropGroup['menu'].add_command(label=choice, command=tk__._setit(sGroup, choice))

def clearArrays():  
    VFvalue.delete(0, 'end')
    VFdate.delete(0,'end')
    sGroup.set('')
    sUser.set('')
    VFdesc.delete(0,'end')
    VFgroup.delete(0,'end')    
    VFID.delete(0,'end')
    

def delID(): 
    if checkID():
        valID = int(VFID.get()) 
        df.drop(valID, inplace = True)
        clearArrays()
        dumpData(df)
        VFID.insert(0,valID)
    
    
def replaceID(): 
    #TODO einträg ändern 
    count = 0
    if checkID():       
        valID = int(VFID.get()) 
        if VFvalue.get() != '':
            df.loc[valID, 'Betrag'] = VFvalue.get()
            count += 1
        if sGroup.get():
            df.loc[valID, 'Oberstruktur'] = sGroup.get()
            count += 1
        if VFdesc.get():
            df.loc[valID, 'Zweck'] = VFdesc.get()
            count += 1
    if count > 0:
        print('ID %i geändert'%valID)
        dumpData(df)
    else:
        print ('Keine Eingaben vorhanden')

def Bank():
    UpdateBankData(True)

if __name__ == '__main__' :
    te = '24.7.2017'
    ro = tk__.Tk()
    df = getDataPyth()    
    #Layout
    ro.geometry("500x350")
    x1 = 5
    x2 = 85
    B = tk__.Button(ro, text ="Betrag einlesen", command = readInValue)
    B.place(x=100,y=220)
    #Save
    B2 = tk__.Button(ro, text ="Del Duplicates", command = FindDuplicates)
    B2.place(x=10,y=220)
    #Eintrag löschen
    Bfind = tk__.Button(ro, text ="Eintrag suchen", command = findIt)
    Bfind.place(x=200,y=220)
    Bclear = tk__.Button(ro, text ="Felder löschen", command =clearArrays)
    Bclear.place(x=250,y=300)
    Bdel = tk__.Button(ro, text ="Eintrag löschen", command =delID)
    Bdel.place(x=x1,y=300)
    Bchage = tk__.Button(ro, text ="Eintrag ändern", command =replaceID)
    Bchage.place(x=x1+100,y=300)
    B_Bank = tk__.Button(ro, text ="Bankdaten aktualisieren", command = Bank )
    B_Bank.place(x=350 ,y=300) 
    LID = tk__.Label(ro, text='ID:')
    VFID = tk__.Entry(ro, bd = 5) #Value Field
    LID.place(x=x1, y= 250)
    VFID.place(x=x1+40, y=250)
    #Betrag  
    Lvalue = tk__.Label(ro, text='Betrag:')
    VFvalue = tk__.Entry(ro, bd = 5) #Value Field
    Lvalue.place(x=x1, y=40)
    VFvalue.place(x=x2, y=40)
    #Datum
    L2 = tk__.Label(ro, text='Datum:')
    VFdate = tk__.Entry(ro, bd = 5) #Value Field
    L2.place(x =x1, y=60)
    VFdate.place(x =x2, y=60)
    #Verwendungszweck
    L3 = tk__.Label(ro, text='Gruppe:')
    L3.place(x =x1, y=85)
    lst1 = df['Oberstruktur'].unique()
    sGroup = tk__.StringVar()
    dropGroup = tk__.OptionMenu(ro,sGroup,*lst1)
    dropGroup.place( x = x2, y=85)   
    B_addgroup = tk__.Button(ro, text ="Gruppe hinzufügen", command = addSome)
    B_addgroup.place(x= x2  + 150 ,y=33)  
    L32 = tk__.Label(ro, text='Gruppe erweitern mit:')
    L32.place(x =x2 + 140, y=60)
    VFgroup = tk__.Entry(ro, bd =5) #Value Field
    VFgroup.place(x =x2 + 140, y=85)
    #Genaue Beschreibung
    L4 = tk__.Label(ro, text='Beschreibung:' )
    VFdesc = tk__.Entry(ro, bd=5, width=50) #Value Field
    L4.place(x =x1, y=110)
    VFdesc.place(x=x2, y=110)
    #Zahler
    L5 = tk__.Label(ro, text='Person:')
    L5.place(x=x1, y=180)
    lst2 = ['Klaus', 'Gina']
    sUser = tk__.StringVar()
    dropUser = tk__.OptionMenu(ro,sUser,*lst2)
    dropUser.place(x=x2, y=180)    
 
    ro.mainloop()


