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
        delID()
        return df

def savetoBase(value, datum, oName, desc, person):
    rowmax = len(df)
    df.loc[rowmax+1] = np.nan
    #tdate = datetime.datetime.strptime(datum,"%d.%m.%Y").date()
    df.loc[rowmax+1, df.columns[0]] = pd.to_datetime(datum, yearfirst = True, format='%d.%m.%Y').date()
    df.loc[rowmax+1, 'Oberstruktur'] = oName
    df.loc[rowmax+1, 'Verwendungszweck'] = str(desc)
    df.loc[rowmax+1, 'Betrag'] = float(value)
    df.loc[rowmax+1, 'Zahlungsart'] = 'BAR'                
    df.loc[rowmax+1, df.columns[1]] = person     
    print ('Eintrag eingetragen')
    dumpData(df)
    return df

'''def FindDuplicates(df):
    for i in np.arange(0,10):#df.index:
        temp = df.loc[df.Betrag == df.loc[i, 'Betrag']]        
        if len(temp)>1:
            print (temp.loc[temp.Buchung == df.loc[i,'Buchung']])
    return temp
'''
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
        print ('Eingabe nicht korrekt, bitte prüfen.')
        OK = False
        #break            
    return OK

def findIt():
    print ('Noch nicht implementiert')

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

def delID():  
    VFvalue.delete(0, 'end')
    VFdate.delete(0,'end')
    sGroup.set('')
    sUser.set('')
    VFdesc.delete(0,'end')
    VFgroup.delete(0,'end')
    print ('Felder gelöscht')
    VFID.delete(0,'end')
    print ('Löschung noch nicht implementiert')    

if __name__ == '__main__' :
    te = '24.7.2017'
    ro = tk__.Tk()
    df = getDataPyth()    
    #Layout
    ro.geometry("400x300")
    x1 = 5
    x2 = 85
    B = tk__.Button(ro, text ="Betrag einlesen", command = readInValue)
    B.place(x=100,y=180)
    #Save
    B2 = tk__.Button(ro, text ="List Duplicates", command = FindDuplicates)
    B2.place(x=10,y=180)
    #Eintrag löschen
    Bfind = tk__.Button(ro, text ="Eintrag suchen", command = findIt)
    Bfind.place(x=200,y=180)
    Bdel = tk__.Button(ro, text ="Eintrag löschen", command =delID)
    Bdel.place(x=200,y=250)
    LID = tk__.Label(ro, text='ID:')
    VFID = tk__.Entry(ro, bd = 5) #Value Field
    LID.place(x = 120, y= 220)
    VFID.place(x =160, y= 220)
    #Betrag  
    Lvalue = tk__.Label(ro, text='Betrag:')
    VFvalue = tk__.Entry(ro, bd = 5) #Value Field
    Lvalue.place(x = x1, y= 40)
    VFvalue.place(x =x2, y= 40)
    #Datum
    L2 = tk__.Label(ro, text='Datum:')
    VFdate = tk__.Entry(ro, bd = 5) #Value Field
    L2.place(x =x1, y= 60)
    VFdate.place(x =x2, y= 60)
    #Verwendungszweck
    L3 = tk__.Label(ro, text='Gruppe:')
    L3.place(x =x1, y= 85)
    lst1 = df['Oberstruktur'].unique()
    sGroup = tk__.StringVar()
    dropGroup = tk__.OptionMenu(ro,sGroup,*lst1)
    dropGroup.place( x = x2, y = 85)   
    B3 = tk__.Button(ro, text ="Gruppe hinzufügen", command = addSome)
    B3.place(x= x2  + 140 ,y= 110)  
    L32 = tk__.Label(ro, text='Gruppe erweitern mit:')
    L32.place(x =x2 + 140, y= 60)
    VFgroup = tk__.Entry(ro, bd = 5) #Value Field
    VFgroup.place(x =x2 + 140, y= 85)
    #Genaue Beschreibung
    L4 = tk__.Label(ro, text='Beschreibung:')
    VFdesc = tk__.Entry(ro, bd = 5) #Value Field
    L4.place(x =x1, y= 110)
    VFdesc.place(x =x2, y= 110)
    #Zahler
    L5 = tk__.Label(ro, text='Person:')
    L5.place(x =x1, y= 140)
    lst2 = ['Klaus', 'Gina']
    sUser = tk__.StringVar()
    dropUser = tk__.OptionMenu(ro,sUser,*lst2)
    dropUser.place( x = x2, y = 140)         
    ro.mainloop()


