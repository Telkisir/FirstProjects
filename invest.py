# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 21:32:17 2017

@author: Telkisir
Investmentrechner:
    Grenzkosten für Immobilienpreis
"""

import pandas as pd
import numpy as np

irate = 0.04 # 
loan_inital = 0.02
loan_second = 0.03 #Refinanzierung nach 10 Jahren

money = 100000
inv = 400000
ownshare = money/inv #%
vlost = 0.02 #FOM
tmax = 40 # Jahre
mrent = 1000
yrent = mrent * 12
inf = 0.02


def invest(i):
    value = inv * ownshare * (1+irate)**i 
    return value

def rent(i):
    value = yrent * (1+inf)**i
    return value

def loan(i):
    if i == 0:
        df_money.loc[i, 'loan'] = (inv * (1 - ownshare)) * (1+loan_inital) - yrent    
    else:
        if i <= 10:
            df_money.loc[i, 'loan'] = df_money.loc[i-1, 'loan'] * (1+loan_inital) -yrent
        else:
            df_money.loc[i, 'loan'] = df_money.loc[i-1, 'loan'] * (1+loan_second) -yrent
    return df_money.loc[i, 'loan']

def immo(i):
    value = inv * (1 - vlost)**i
    
    return value

df_money = pd.DataFrame(index = np.arange(0, tmax), columns = ['sum','loan','invest', 'immo']).astype(float)
# Fall 1
#Ich investiere das geld in Rentenpapier und zahle Miete
#Fall 2
#Ich kaufe mir eine Immobolie, spare Miete

for i in range(0, tmax):
    #df_money.loc[i, 'rent'] = -yrent * (1+inf)**i
    if i == 0:
        df_money.loc[i, 'loan'] = -(inv * (1 - ownshare)) * (1+loan_inital) + yrent * (1+inf)**i    
    else:
        if i <= 10:
            df_money.loc[i, 'loan'] = df_money.loc[i-1, 'loan'] * (1+loan_inital) +yrent * (1+inf)**i
        else:
            df_money.loc[i, 'loan'] = df_money.loc[i-1, 'loan'] * (1+loan_second) +yrent * (1+inf)**i
    df_money.loc[i, 'invest']  = - inv * ownshare * (1+irate)**i 
    df_money.loc[i, 'immo']  = inv * (1 - vlost)**i
    df_money.loc[i, 'sum']  = df_money.loc[i,:].sum()
    #df_money.loc[i, 'sum'] = immo(i) - df_money.loc[i, 'loan'] - df_money.loc[i, 'case1']
    i =+ 1
    #print (npv[i], i)



