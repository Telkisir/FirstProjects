# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 18:30:50 2016

@author: Telkisir
"""
import pprint
#Sotieren per Hand
def SortArray(): # Laufzeit n/2 * (n+1)

    lTest = [ 3, 5, 1, 9, 3, 77, 433, 5, 5, 5, 6, 111,  9]
    
    x=0 
    y=0
    iZaehler = 0
    for x in range(0,len(lTest),1):
        iMin = lTest[x]
        for y in range(x,len(lTest),1):
            if iMin > lTest[y] :
                lTest[x] = lTest[y]
                lTest[y] = iMin
                iMin = lTest[x]
                
            iZaehler += 1
                
    print ("Für ein Array mit " + str(len(lTest)) + " Eintraege wurden " 
           +str(iZaehler) +" Durchläufe benötigt")


def ch4_ex1():
    lNames = ['apples', 'bananas', 'tofu', 'cats', 'fish']
    sList= ''
    for i in range(len(lNames)-1):
        sList = sList + lNames[i] + ", "
    sList = sList + "and " + lNames[len(lNames)-1] 
    print (sList)
    
def ch5_print():
    message = 'It was a bright cold day in April, and the clocks were striking thirteen.'
    count = {}
    for character in message:
        count.setdefault(character, 0)
        count[character] = count[character] + 1
    
    print(count)
    pprint.pprint(count)
    print(pprint.pformat(count))

def printBoard(board):
    print(board['top-L'] + '|' + board['top-M'] + '|' + board['top-R'])
    print('-+-+-')
    print(board['mid-L'] + '|' + board['mid-M'] + '|' + board['mid-R'])
    print('-+-+-')
    print(board['low-L'] + '|' + board['low-M'] + '|' + board['low-R'])
    printBoard(theBoard)
#main
def tictactoe():
    theBoard = {'top-L': ' ', 'top-M': ' ', 'top-R': ' ',
                'mid-L': ' ', 'mid-M': ' ', 'mid-R': ' ',
                'low-L': ' ', 'low-M': ' ', 'low-R': ' '}
                
                


def totalBrought(guests, item):
    numBrought = 0
    for k, v in guests.items():
         numBrought = numBrought + v.get(item, 0)
    return numBrought
#>>> spam = {'color': 'red', 'age': 42}
#>>> for k, v in spam.items():
#        print('Key: ' + k + ' Value: ' + str(v))    
#Key: age Value: 42
#Key: color Value: red
def printBrought():
    allGuests = {'Alice': {'apples': 5, 'pretzels': 12},
                'Bob': {'ham sandwiches': 3, 'apples': 2},
                'Carol': {'cups': 3, 'apple pies': 1}}
    print('Number of things being brought:')
    print(' - Apples         ' + str(totalBrought(allGuests, 'apples')))
    print(' - Cups           ' + str(totalBrought(allGuests, 'cups')))
    print(' - Cakes          ' + str(totalBrought(allGuests, 'cakes')))
    print(' - Ham Sandwiches ' + str(totalBrought(allGuests, 'ham sandwiches')))
    print(' - Apple Pies     ' + str(totalBrought(allGuests, 'apple pies')))
    
#main

ch5_print()

