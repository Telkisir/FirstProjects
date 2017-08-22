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
            Rundfunk | Mobilfunkrechnung|\d{14}-\d{8}|
            Nebenkostenabrechnung
            )''',re.IGNORECASE | re.VERBOSE)
    InsuranceRegex = re.compile(r'''(
            Hausrat | Versicherung | Reiseschutz|^WWK.
            )''',re.IGNORECASE | re.VERBOSE)    
    FoodRegex = re.compile(r'''(
            Aldi |Lidl| REWE|\sEDEKA\s|Penny
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
            ^GA\sING |^Hochzeit | Finanzierung|Ruecklagen|Rücklagen
            )''',re.IGNORECASE | re.VERBOSE)      
    AutoRegex = re.compile(r'''(
            ^Markant\sTS |^Aral|^SB-Tank|^Westfalen\sTS|^ADAC|^KFZ|^HEM|Flixbus|Gottschalk
            )''',re.IGNORECASE | re.VERBOSE)
    ClothRegex = re.compile(r'''(
            Schuhe|^CA|^Decathlon|^Jack\sWolfskin
            )''',re.IGNORECASE | re.VERBOSE) 
    FreeRegex = re.compile(r'''(
            Sauna|^Miniatur|^Decathlon|^Spielbar|
            ^Reitbeteiligung
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
            ^CCV\.Bastion\shotel| Reisekosten | Kassenzeichen | ^MOtel one Wien | ^Hotel Wartburg
            )''',re.IGNORECASE | re.VERBOSE)   
    HealthRegex = re.compile(r'''(
            Malteser-Apotheke | Fielmann
            )''',re.IGNORECASE | re.VERBOSE) 
    dicOberstruktur = {'Arbeit':ArbeitRegex, 'Gesundheit':HealthRegex, 'Urlaub':UrlaubRegex, 'Bienen': BeeRegex, 'Freizeit': FreeRegex, 'Diverses': DivRegex,'Kleidung': ClothRegex, 'Auto':AutoRegex,'Umbuchung': UmbuchungenRegex , 'Kaltmiete': KaltRegex, 'Nebenkosten': NBKRegex, 'Versicherung': InsuranceRegex, 'Essen': FoodRegex, 'Einnahmen': IncomeRegex, 'Sonstige':SonstigRegex}
    return dicOberstruktur

def getFilterBankAuftrag():
    InsRegex = re.compile(r'''(
            ^AAchenmuenchener
            )''',re.IGNORECASE | re.VERBOSE) 
    FoodRegex = re.compile(r'''(
            ^Netto|^Dursty
            )''',re.IGNORECASE | re.VERBOSE)   
    AutoRegex = re.compile(r'''(
            ^Jet|SB\sTank|^Franz\sSchulze
            )''',re.IGNORECASE | re.VERBOSE)  
    SonstigRegex = re.compile(r'''(
            REAL|^Yves|IKEA|^HIT|^Ann\sSayed|^Stadt\sH.\sRath|
            ^Rossmann|^Easybuy|^GARTENC\.CRUMBACH |^Bauhaus
            )''',re.IGNORECASE | re.VERBOSE)  
    HealthRegex = re.compile(r'''(
            ^Zieten|Constanze\sSchneider|^Fielmann
            )''',re.IGNORECASE | re.VERBOSE)  
    TeleRegex  = re.compile(r'''(
            Sipgate|^1u1
            )''',re.IGNORECASE | re.VERBOSE)  
    ArbeitRegex  = re.compile(r'''(
            ^Hotel\sDress|^Kasse\sder\sRWTH\sAAchen|^ZA\sAG|^Eugen|^Stadtkasse\sItzehoe
            )''',re.IGNORECASE | re.VERBOSE)   
    VereinRegex  = re.compile(r'''(
            Physikalische|Schwimmverein|^Verein\sDeutscher\sIngenieure
            )''',re.IGNORECASE | re.VERBOSE)  
    SpendeRegex  = re.compile(r'''(
            ^^SOS
            )''',re.IGNORECASE | re.VERBOSE)   
    FreeRegex  = re.compile(r'''(
            ^Visa\sSocialdeal|^Spielbar
            )''',re.IGNORECASE | re.VERBOSE)
    ClothRegex  = re.compile(r'''(
            ^Siemes|H\+M|^Reno|^Lust\sfor\slife|
            Robert\sLey\sHer
            )''',re.IGNORECASE | re.VERBOSE)
    BeeRegex  = re.compile(r'''(
            ^Tierseuchenkasse|^Bienenfreunde
            )''',re.IGNORECASE | re.VERBOSE)
    UmbRegex  = re.compile(r'''(
            ^Klaus\sBiss
            )''',re.IGNORECASE | re.VERBOSE)
    WedRegex  = re.compile(r'''(
            ^Schauinsland|^Stadt\sWitten|Gasthauss\sHerrig|^Felsenland|^Bijou|
            ^The\sJeweller|^Listmann|^Action|
            ^Markus\sEnglmeier
            )''',re.IGNORECASE | re.VERBOSE)
    dicFilterBank2 = {'Umbuchung':UmbRegex,'Gesundheit':HealthRegex,'Vereine':VereinRegex, 'Hochzeit': WedRegex,'Bienen':BeeRegex ,'Kleidung':ClothRegex, 'Freizeit': FreeRegex, 'Spende': SpendeRegex, 'Arbeit': ArbeitRegex, 'Auto':AutoRegex, 'Sonstige': SonstigRegex, 'Nebenkosten': TeleRegex, 'Versicherung': InsRegex, 'Essen': FoodRegex}
    return dicFilterBank2

