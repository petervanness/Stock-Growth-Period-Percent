import datetime
import pandas as pd
import yfinance as yf

#--------set parameters for stocks to pull, over what period and interval for analysis:
# tickers = input("Enter desired tickers ('AA BB CC'):")
# period_start = input('Enter analysis period start date as YYYY-MM-DD:')
# period_end = input('Enter analysis period end date as YYYY-MM-DD:')
# # measure = input('Enter measure for analysis (Open, Close, High, Low, Volume, Adj Close):')
# interval = input('Enter interval for analysis (Day, Week, Month or Quarter):')

#easier to develop without entering by user input prompt
tickers = 'GOOGL CDXS'
period_start = '2016-01-01'
period_end = '2020-05-31'
measure = 'Close'
interval = 'Week'

# Adjust strings to allow for varied capitalization
measure = measure.capitalize()
interval = interval.capitalize()

# Download data --
# Always included DJI because for now I need multiple tickers to keep consistent data structure (namely, ticker label)
df = yf.download(tickers='^DJI '+tickers, start=period_start,end=period_end, group_by = 'column')
df['Date'] = df.index
df = df.melt(id_vars = 'Date')
df = df.rename(columns={'variable_0':'Measure','variable_1':'Ticker'})

#---create broader time vars (e.g. where Date = 2/16/2021, week is Friday-ending, so 2/19/2021, month = 2/01/2021, and quarter = Q1)
df['Date'] = pd.to_datetime(df['Date'])
df['Day'] = df['Date']
from pandas.tseries.offsets import *
df['Week'] = df['Date'].where( df['Date'] == (( df['Date'] + Week(weekday=4) ) - Week()), df['Date'] + Week(weekday=4))
df['Month'] = df['Date'].dt.to_period('M').dt.to_timestamp()
df['Quarter'] = pd.PeriodIndex(df.Date, freq='Q')

#set interval beginning and end
min = df.groupby([interval])[['Date']].min()
min = min.rename(columns={'Date':'Min Date'})

max = df.groupby([interval])[['Date']].max()
max = max.rename(columns={'Date':'Max Date'})

#merge min and max with og data so that subsetting is easy
df = pd.merge(df, min, how='left', on=interval)
df = pd.merge(df, max, how='left', on=interval)

#select just opening and closing values for each period and ticker
open = df.loc[df['Measure']=='Open']
open = open.loc[open['Date']==open['Min Date']]
open= open.rename(columns={'value':'Open'})
open = open.filter(['Ticker', interval, 'Min Date', 'Open'], axis=1)

close = df.loc[df['Measure']==measure]
close = close.loc[close['Date']==close['Max Date']]
close= close.rename(columns={'value':'Close'})
close = close.filter(['Ticker', interval, 'Max Date', 'Close'], axis=1)
comp = pd.merge(open, close, how = 'left', on=[interval, 'Ticker'])

#create flag when period close is higher than period open
comp['Growth_period'] = 0

for i, row in comp.iterrows():
    if comp.loc[i,'Close'] > comp.loc[i,'Open']:
        comp.loc[i,'Growth_period'] = 1

#count the number of periods with growth and number of total periods
count = comp.groupby(['Ticker'])[['Ticker']].count()
count=count.rename(columns={'Ticker':'Periods'})
sum = comp.groupby(['Ticker'])[['Growth_period']].sum()

#merge growth and count sums; calculate pct of intervals with growth
comp_out = pd.merge(sum,count, how = 'left', on='Ticker')
comp_out['Grow_period_pct'] = comp_out['Growth_period']/comp_out['Periods']
comp_out['period_start'] = period_start
comp_out['period_end'] = period_end
comp_out['Growth_Interval'] = interval
print(comp_out)
