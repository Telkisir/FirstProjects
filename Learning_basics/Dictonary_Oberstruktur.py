# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 17:44:03 2016

@author: Telkisir
"""

# Demo file for Spyder Tutorial
# Hans Fangohr, University of Southampton, UK
import re

# main program starts here
def getFilterBankVerw():
    KaltRegex = re.compile(r'Miete')
    '''
                    ( #Nebenkosten
                     Miete.?+  |    # charater class username
                     Lohn
                     )'', re.VERBOSE)
    '''   
    NBKRegex = re.compile(r'''(
            Strom | Stromio | Energieversorgung | #Strom
            simyo | telefon | Unitymedia | Prepaid |
            Rundfunk | Mobilfunkrechnung|\d{14}-\d{8}
            )''',re.IGNORECASE | re.VERBOSE)
    InsuranceRegex = re.compile(r'''(
            Hausrat | Versicherung | Reiseschutz|^WWK.
            )''',re.IGNORECASE | re.VERBOSE)    
    FoodRegex = re.compile(r'''(
            Aldi | Lidl | REWE|\sEDEKA\s|Penny
            )''',re.IGNORECASE | re.VERBOSE)
    IncomeRegex = re.compile(r'''(
            Gehalt | Rente |
            Q66953584
            )''',re.IGNORECASE | re.VERBOSE)
    SonstigRegex = re.compile(r'''(
            Elbenwald | NICI | #Geschenke  
            Ebay |^DM\sFIL|Saturn|Kerkrade
            )''',re.IGNORECASE | re.VERBOSE)
    UmbuchungenRegex = re.compile(r'''(
            ^GA\sING | Hochzeit | Finanzierung
            )''',re.IGNORECASE | re.VERBOSE)      
    AutoRegex = re.compile(r'''(
            ^Markant\sTS |^Aral|^SB-Tank|^Westfalen\sTS|^ADAC|^KFZ|^HEM|Flixbus
            )''',re.IGNORECASE | re.VERBOSE)
    ClothRegex = re.compile(r'''(
            Schuhe|^CA
            )''',re.IGNORECASE | re.VERBOSE) 
    FreeRegex = re.compile(r'''(
            Sauna|^Miniatur|^Decathlon|^Spielbar
            )''',re.IGNORECASE | re.VERBOSE) 
    BeeRegex = re.compile(r'''(
            ^Geller|^Honigkurs
            )''',re.IGNORECASE | re.VERBOSE) 
    DivRegex = re.compile(r'''(
            notting
            )''',re.IGNORECASE | re.VERBOSE)         
    UrlaubRegex = re.compile(r'''(
            Nunspeet
            )''',re.IGNORECASE | re.VERBOSE)  
    ArbeitRegex  = re.compile(r'''(
            ^CCV\.Bastion\shotel
            )''',re.IGNORECASE | re.VERBOSE)   
    dicOberstruktur = {'Arbeit':ArbeitRegex, 'Urlaub':UrlaubRegex, 'Bienen': BeeRegex, 'Freizeit': FreeRegex, 'Diverses': DivRegex,'Kleidung': ClothRegex, 'Auto':AutoRegex,'Umbuchung': UmbuchungenRegex , 'Kaltmiete': KaltRegex, 'Nebenkosten': NBKRegex, 'Versicherung': InsuranceRegex, 'Essen': FoodRegex, 'Einnahmen': IncomeRegex, 'Sonstige':SonstigRegex}
    return dicOberstruktur

def getFilterBankAuftrag():
    InsRegex = re.compile(r'''(
            ^AAchenmuenchener
            )''',re.IGNORECASE | re.VERBOSE) 
    FoodRegex = re.compile(r'''(
            ^Netto|^Dursty
            )''',re.IGNORECASE | re.VERBOSE)   
    AutoRegex = re.compile(r'''(
            ^Jet|SB\sTank
            )''',re.IGNORECASE | re.VERBOSE)  
    SonstigRegex = re.compile(r'''(
            REAL|^Yves|IKEA|^HIT|^Ann\sSayed|^Stadt\sH.\sRath|
            ^Rossmann|^Easybuy
            )''',re.IGNORECASE | re.VERBOSE)  
    HealthRegex = re.compile(r'''(
            ^Zieten
            )''',re.IGNORECASE | re.VERBOSE)  
    TeleRegex  = re.compile(r'''(
            Sipgate|^1u1
            )''',re.IGNORECASE | re.VERBOSE)  
    ArbeitRegex  = re.compile(r'''(
            ^Hotel\sDress|Kasse\sder\sRWTH\sAAchen|^ZA\sAG|^Eugen
            )''',re.IGNORECASE | re.VERBOSE)   
    VereinRegex  = re.compile(r'''(
            Physikalische|Schwimmverein
            )''',re.IGNORECASE | re.VERBOSE)  
    SpendeRegex  = re.compile(r'''(
            ^^SOS
            )''',re.IGNORECASE | re.VERBOSE)   
    FreeRegex  = re.compile(r'''(
            ^Visa\sSocialdeal
            )''',re.IGNORECASE | re.VERBOSE)
    ClothRegex  = re.compile(r'''(
            ^Siemes|H\+M
            )''',re.IGNORECASE | re.VERBOSE)
    BeeRegex  = re.compile(r'''(
            ^Tierseuchenkasse|^Bienenfreunde
            )''',re.IGNORECASE | re.VERBOSE)
    WedRegex  = re.compile(r'''(
            ^Schauinsland|^Stadt\sWitten|Gasthauss\sHerrig|^Felsenland|^Bijou
            )''',re.IGNORECASE | re.VERBOSE)
    UmbRegex  = re.compile(r'''(
            ^Klaus\sBiss
            )''',re.IGNORECASE | re.VERBOSE)
    dicFilterBank2 = {'Umbuchung':UmbRegex,'Gesundheit':HealthRegex,'Vereine':VereinRegex, 'Hochzeit': WedRegex,'Bienen':BeeRegex ,'Kleidung':ClothRegex, 'Freizeit': FreeRegex, 'Spende': SpendeRegex, 'Arbeit': ArbeitRegex, 'Auto':AutoRegex, 'Sonstige': SonstigRegex, 'Nebenkosten': TeleRegex, 'Versicherung': InsRegex, 'Essen': FoodRegex}
    return dicFilterBank2