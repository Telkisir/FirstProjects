# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 21:25:37 2017

@author: Telkisir

Check Gaunlet
"""

import pandas as pd, numpy as np
from numpy import array


def chance(df, opponent):
    
    return 0


charName = ['char1', 'char2','char3']
colName = ['Low1', 'High1', 'Low2', 'High2', 'crit']

values = [[150, 235, 233, 342, 0.45],
          [150, 235, 233, 342, 0.45],
          [150, 235, 233, 342, 0.45]]

values2 = array(values)
values2 = values2.reshape(3,5)

df = pd.DataFrame(values2, index= charName, columns=colName)

opponent = [150, 235, 233, 342, 0.45]

