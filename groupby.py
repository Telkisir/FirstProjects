# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 21:20:57 2017

@author: Telkisir
Test groubpy
"""
import pandas as pd, numpy as np

df = pd.DataFrame({'A' : ['foo', 'bar', 'foo', 'bar',
                             'foo', 'bar', 'foo', 'foo'],
                      'B' : ['one', 'one', 'two', 'three',
                             'two', 'two', 'one', 'three'],
                       'C' : np.random.randn(8),
                      'D' : np.random.randn(8)})


def get_letter_type(letter):
    if letter.lower() in 'aeiou':
             return 'vowel'
    else:
             return 'consonant'
    
grouped = df.groupby('A')



