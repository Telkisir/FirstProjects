# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 17:10:02 2017

@author: K. Biß
Project 2
pip install googlefinance



smybol collected by
https://www.boerse-stuttgart.de/de/Sunwin-Stevia-Aktie-US86803D1090

Quelle:
http://help.quandl.com/article/68-is-there-a-rate-limit-or-speed-limit-for-api-usage

exchange-abbraviations:
https://finance.yahoo.com/lookup/all?s=Ingenico&t=A&m=ALL&r=
https://github.com/Benny-/Yahoo-ticker-symbol-downloader

Downloader data:
https://pypi.python.org/pypi/ystockquote/
"""
import pandas as pd
import pandas_datareader.data as wb
from pandas_datareader._utils import RemoteDataError
import numpy as np
import pickle


def getDataSingle(ticker):
    import datetime
    now = datetime.datetime.now()
    start_date = '2007-01-02'
    end_date = now.strftime("%Y-%m-%d")
    data_source = 'yahoo'
    data = wb.DataReader(ticker, data_source, start_date, end_date)
    all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')
    data = data.reindex(all_weekdays).fillna(method='ffill')
    data.reset_index(inplace=True)
    data.rename(columns={u'Adj Close': 'AdjClose',
                         u'index': 'Date'}, inplace=True)
    return data


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
    data = findData(ticker)
    if data is None:
        print('Keine Daten für %s' % ticker.split(sep='.')[0])
        return dftickers
    else:
        print('Dataset %s wird geprüft' % ticker)
    m200 = np.float32(data.AdjClose.rolling(window=200).mean()[-1:])
    m20 = np.float32(data.AdjClose.rolling(window=20).mean()[-1:])
    m10 = np.float32(data.AdjClose.rolling(window=10).mean()[-1:])
    m5 = np.float32(data.AdjClose.rolling(window=5).mean()[-1:])
    lval = data.AdjClose[-1:].iloc[0]
    if (data.AdjClose[-20:] > lval).any():
        dftickers.loc[pos, 'M1Regel'] = 'No'
    else:
        dftickers.loc[pos, 'M1Regel'] = 'Yes'
    if m20 < m10 < m5:
        dftickers.loc[pos, 'CrossMA'] = 'Yes'
    else:
        dftickers.loc[pos, 'CrossMA'] = 'No'
    if m200 < lval:
        dftickers.loc[pos, 'CrossMA200'] = 'Up'
    else:
        dftickers.loc[pos, 'CrossMA200'] = 'Down'
    dftickers.loc[pos, 'LastUpdate'] = data.Date[-1:].iloc[0]
    dftickers.loc[pos, 'Pvalue'] = lval
    return dftickers


def UpdateJournal(raw=True):
    if raw:
        dftickers = getListOrigin()
    else:
        dftickers = getListUpdated()
    for index in dftickers.index:
        ticker = dftickers.Ticker.loc[index]
        dftickers = checkStock(dftickers, ticker, index)
    pickle.dump(dftickers, open('dftickers.p', 'wb'))
    return dftickers


def setFazit(dftickers):
    print('TODO')
    '#TODO'


def getListUpdated():
    return pickle.load(open('Journal.p', 'rb'))


def findData(ticker):
    symbols = pickle.load(open('stocks.p', 'rb'))
    stocksym = ticker.split(sep='.')[0]
    exchange = list(symbols.loc[symbols.Ticker.str.contains(stocksym),
                                'Ticker'])
    for place in exchange:
        try:
            data = getDataSingle(place)
            return data
        except RemoteDataError:
            print('Data nicht einlesbar für Symbol %s' % place)
    return


def setSymbols():
    symbols = pd.read_excel('stocks.xlsx')
    pickle.dump(symbols, open('stocks.p', 'wb'))


'''
#######Sehr gute Seite#########
#http://www.learndatasci.com/python-finance-part-yahoo-finance-api-pandas-matplotlib/


# Getting just the adjusted closing prices. This will return a Pandas DataFrame
# The index in this DataFrame is the major index of the panel_data.
close = panel_data.ix['Close']

# Getting all weekdays between 01/01/2000 and 12/31/2016
all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')

# How do we align the existing prices in adj_close with our new set of dates?
# All we need to do is reindex close using all_weekdays as the new index
close = close.reindex(all_weekdays)

close.head(10)

# Getting just the adjusted closing prices. This will return a Pandas DataFrame
# The index in this DataFrame is the major index of the panel_data.
adj_close = panel_data.ix['Close']

# Getting all weekdays between 01/01/2000 and 12/31/2016
all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')

# How do we align the existing prices in adj_close with our new set of dates?
# All we need to do is reindex adj_close using all_weekdays as the new index
adj_close = adj_close.reindex(all_weekdays)

# Reindexing will insert missing values (NaN) for the dates that were not present
# in the original set. To cope with this, we can fill the missing by replacing them
# with the latest available price for each instrument.
adj_close = adj_close.fillna(method='ffill')

# Get the MSFT time series. This now returns a Pandas Series object indexed by date.
msft = adj_close.ix[:, 'MSFT']
# Calculate the 20 and 100 days moving averages of the closing prices
short_rolling_msft = msft.rolling(window=20).mean()
long_rolling_msft = msft.rolling(window=100).mean()

# Plot everything by leveraging the very powerful matplotlib package
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(msft.index, msft, label='MSFT')
ax.plot(short_rolling_msft.index, short_rolling_msft, label='20 days rolling')
ax.plot(long_rolling_msft.index, long_rolling_msft, label='100 days rolling')
ax.set_xlabel('Date')
ax.set_ylabel('Adjusted closing price ($)')
ax.legend()
'''
