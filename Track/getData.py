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

"""

import webbrowser
import requests
import googlefinance, json
import pandas_datareader.data as wb
import datetime

from googlefinance import getQuotes
#google finance get historical data python


date_start = datetime.datetime(2016,1,1) #good
date_end   = datetime.date.today() #good



address = 'http://www.boerse.de/historische-kurse/Siemens-Aktie/DE0007236101'
webbrowser.open(address)
res = requests.get(address)

wkn = '723610' # stock symbol VOW3
symbol = 'VOW3'
symbol = 'M5Z' #'Manz'
symbol = 'AAPL'
print (json.dumps(getQuotes(symbol)))


from yahoo_finance import Share
yahoo = Share(symbol)




#https://stackoverflow.com/questions/44136765/python-using-google-finance-to-download-index-data
import pandas as pd
from pandas_datareader import data as web   
import datetime
start = datetime.datetime(2016,1,1)
end   = datetime.date.today()
apple = web.DataReader('aapl', 'google', start, end)


#https://stackoverflow.com/questions/44080070/google-finance-historical
import pandas_datareader.data as wb
web_df = wb.DataReader(symbol, 'google', date_start, date_end) #works for AAPL but not for the others

#https://stackoverflow.com/questions/10040954/alternative-to-google-finance-api
address = 'http://finance.yahoo.com/d/quotes.csv?s=AAPL+GOOG+MSFT&f=sb2b3jk'
webbrowser.open(address)

''' Sehr gute Seite'''
#http://www.learndatasci.com/python-finance-part-yahoo-finance-api-pandas-matplotlib/
from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
import yahoo_finance
import fix_yahoo_finance 


# Define the instruments to download. We would like to see Apple, Microsoft and the S&P500 index.
tickers = ['AAPL', 'MSFT', 'XSDG', 'AMZ', 'WCH']
           #'VOW3', 'ABEA', 'GEC']

# Define which online source one should use
data_source = 'yahoo'

# We would like all available data from 01/01/2000 until 12/31/2016.
start_date = '2010-01-01'
end_date = '2016-12-31'

# User pandas_reader.data.DataReader to load the desired data. As simple as that.
panel_data = data.DataReader(tickers, data_source, start_date, end_date)



data_source = 'google'
panel_data = data.DataReader(tickers, data_source, start_date, end_date)

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


#https://stackoverflow.com/questions/44112403/yahoo-finance-api-url-not-working-python-fix-for-pandas-datareader
import pandas_datareader.data as pdweb
from pandas_datareader import data as pdr
start_date = '2010-01-01'
end_date = '2016-12-31'
data1 = pdr.get_data_yahoo('AAPL',start_date, end_date)
data2 = pdr.get_data_yahoo(['AAPL','GEC', 'MSFT', 'XSDG', 'AMZ', 'WCH'],start_date, end_date, as_panel=False)
