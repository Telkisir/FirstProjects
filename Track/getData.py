# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 17:10:02 2017

@author: K. Biß
Project 2

smybol collected by
https://www.boerse-stuttgart.de/de/Sunwin-Stevia-Aktie-US86803D1090

exchange-abbreviations:
https://finance.yahoo.com/lookup/all?s=Ingenico&t=A&m=ALL&r=
https://github.com/Benny-/Yahoo-ticker-symbol-downloader

Downloader data:
https://pypi.python.org/pypi/ystockquote/

Similar code:
#http://www.learndatasci.com/python-finance-part-yahoo-finance-api-pandas-matplotlib/
"""
import pandas as pd
import pandas_datareader.data as wb
from pandas_datareader._utils import RemoteDataError
import numpy as np
import pickle
import os
import fnmatch


def getDataSingle(ticker):
    import datetime
    now = datetime.datetime.now()
    start_date = '2007-01-02'
    end_date = now.strftime("%Y-%m-%d")
    all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')
    data_source = 'yahoo'
    pDic = fnmatch.filter(os.listdir(os.path.join(os.getcwd(), 'Data')), '*.p')
    if ticker+'.p' in pDic:
        data = pickle.load(open(os.path.join(os.getcwd(), 'Data', ticker+'.p'), 'rb'))
        start_date = max(data.Date+datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        tmp = DataReader(ticker, data_source, start_date, end_date)
        data = data.append(tmp)
        up = True
    else:
        data = DataReader(ticker, data_source, start_date, end_date)
        up = False
    data.drop_duplicates(inplace=True, subset=['Date'])
    data.index = data.Date
    data = data.reindex(all_weekdays).fillna(method='ffill')
    data.reset_index(drop=True, inplace=True)
    dumpStock(data, ticker, up)
    return data


def dumpStock(df, ticker, up):
    path = os.path.join(os.getcwd(), 'Data')
    if up:
        data = pickle.load(open(os.path.join(path, ticker+'.p'), 'rb'))
        if len(data) >= len(df):
            print('Keine neuen Daten dazugekommen für %s.' % ticker)
            return
    df.drop(df.loc[df.isnull().any(axis=1)].index, inplace=True)
    pickle.dump(df, open(os.path.join(path, ticker+'.p'), 'wb'))


def DataReader(ticker, data_source, start_date, end_date):
    df = wb.DataReader(ticker, data_source, start_date, end_date).reset_index()
    df.rename(columns={u'Adj Close': 'AdjClose',
                         u'index': 'Date'}, inplace=True)
    return df


def getListOrigin():
    import os
    pw = os.path.join('E:', 'Finanzen', 'Aktienhandel',
                      'Aktienjournal_symbol.xls')
    dftickers = pd.read_excel(pw, sheetname='Symbols')
    dftickers.drop(dftickers.loc[dftickers.Ticker.isnull()].index,
                                 inplace=True)
    dftickers.set_index(np.arange(0, len(dftickers)), inplace=True)
    return dftickers


def checkStock(dftickers, ticker, pos):
    data, ticker = findData(ticker)
    if data is None:
        print('Keine Daten für %s' % ticker.split(sep='.')[0])
        return dftickers
    else:
        print('Dataset %s wird geprüft' % ticker)
    m200 = np.float32(data.AdjClose.rolling(window=200).mean()[-1:])[0]
    m20 = np.float32(data.AdjClose.rolling(window=20).mean()[-1:])[0]
    m10 = np.float32(data.AdjClose.rolling(window=10).mean()[-1:])[0]
    m5 = np.float32(data.AdjClose.rolling(window=5).mean()[-1:])[0]
    lval = data.AdjClose[-1:].iloc[0]
    if (data.AdjClose[-20:] > lval).any():
        dftickers.loc[pos, 'M1Regel'] = 'No'
    else:
        dftickers.loc[pos, 'M1Regel'] = 'Yes'
    if m20 < m10 < m5:
        dftickers.loc[pos, 'CrossMA'] = 'Yes'
    elif m20 > m10 > m5:
        dftickers.loc[pos, 'CrossMA'] = 'No'
    else:
        dftickers.loc[pos, 'CrossMA'] = 'no signal'
    dftickers.loc[pos, 'CrossMA200'] = m200
    dftickers.loc[pos, 'LastUpdate'] = data.Date[-1:].iloc[0].strftime('%Y-%m-%d')
    dftickers.loc[pos, 'Pvalue'] = lval
    return dftickers


def UpdateJournal(raw=False):
    if raw:
        dftickers = getListOrigin()
    else:
        dftickers = getJournal()
    for index in dftickers.index:
        ticker = dftickers.Ticker.loc[index]
        dftickers = checkStock(dftickers, ticker, index)
        dftickers = setFazit(dftickers)
    dumpJournal(dftickers)
    return dftickers


def setFazit(dftickers):
    dftickers['PrevFazit'] = dftickers['Fazit']
    dftickers.Fazit = 'no data'
    dftickers.loc[(dftickers.M1Regel == 'Yes') &
                  (dftickers.CrossMA == 'Yes') &
                  (dftickers.CrossMA200 < dftickers.Pvalue),
                  'Fazit'] = 'Buy'
    dftickers.loc[(dftickers.M1Regel == 'No') &
                  (dftickers.CrossMA == 'Yes') &
                  (dftickers.CrossMA200 < dftickers.Pvalue),
                  'Fazit'] = 'Upward trend initalized'
    dftickers.loc[(dftickers.M1Regel == 'No') &
                  (dftickers.CrossMA == 'No') &
                  (dftickers.CrossMA200 > dftickers.Pvalue),
                  'Fazit'] = 'Big fall..look'
    dftickers.loc[(dftickers.Fazit == 'no data'), 'Fazit'] = 'no glue'
    return dftickers


def dumpJournal(dftickers):
    import datetime
    tdate = datetime.datetime.today().date()
    pickle.dump(dftickers,
                open(os.path.join(os.getcwd(),
                                  'Journal_%s%s%s.p'
                                  % (tdate.year, tdate.strftime('%m'),
                                     tdate.strftime('%d'))), "wb"))


def getJournal():
    # Suche mir die aktuellste Datei
    import fnmatch
    import re
    pDic = fnmatch.filter(os.listdir(os.getcwd()), 'Journal*.p')
    dateRegex = re.compile(r'(\d{8})\.p')
    localPlace = 0
    for i in range(0, len(pDic)):
        if re.search(dateRegex, pDic[i]) is not None:
            temp = int(re.search(re.compile(r'(\d{8})'), pDic[i]).group())
            if temp > localPlace:
                localPlace = temp
    df = pickle.load(open(os.path.join(os.getcwd(), 'Journal_'
                                       + str(localPlace)+'.p'), 'rb'))
    df.index = range(0, len(df))
    print('Datum der Journal-Datei ist %s' % str(localPlace))
    return df


def findData(ticker):
    # symbols = pickle.load(open('stocks.p', 'rb'))
    stocksym = ticker.split(sep='.')[0]
    exchange = ['.F', '.SG', '.MU', '.BE', '.DU', '.HM', '.HA', '.EX']
    # exchange = list(symbols.loc[symbols.Ticker.str.contains(stocksym),
    #                             'Ticker'])
    # exchange.sort()
    # exchange =[i for i in exchange if not ('.BE' in i or '.DU' in i)]
    for place in exchange:
        try:
            data = getDataSingle(stocksym + place)
            return data, stocksym + place
        except RemoteDataError:
            print('Data nicht einlesbar für Symbol %s' % stocksym + place)
    return None, stocksym


def setSymbols():
    symbols = pd.read_excel('stocks.xlsx')
    symbols.drop(symbols.loc[symbols.Name.isnull()].index, inplace=True)
    pickle.dump(symbols, open('stocks.p', 'wb'))


def plotStock(ticker):
    import matplotlib.pyplot as plt
    data = findData(ticker)
    small = 50
    large = 200
    short_rolling = data.AdjClose.rolling(window=small).mean()
    long_rolling = data.AdjClose.rolling(window=large).mean()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(data.Date, data.AdjClose, label=ticker)
    ax.plot(data.Date, short_rolling, label='MA'+str(small))
    ax.plot(data.Date, long_rolling, label='MA'+str(large))
    ax.set_xlabel('Date')
    ax.set_ylabel('Adjusted closing price')
    ax.legend()
