# Stock-Growth-Period-Percent
Calculates percentage of periods in which selected stocks grew in a selected time span

A basic program using the yfinance package to calculate percentage of periods in which a stock grew in a selected time span. The general idea is oriented towards options trading
because the inputs for the percentage are a binary calculation: up or down, rather than any specific value change.  

The parameters necessary to run are the stock tickers selected to analyze, period start, period end, measure (e.g. opening vs closing price), and interval of up-down measurement. 
For example, if the folowing parameters were entered:
```
tickers = 'CVX'
period_start = '2015-01-01'
period_end = '2015-05-31'
measure = 'Close'
interval = 'Week'
```

The following data would be pulled and used to calculate the percentage of periods with growth:
```
Ticker	    Month	Min Date	Open	          Max Date	  Close	      Growth_period
CVX	    1/1/2015	1/2/2015	111.6299973	  1/30/2015	  102.5299988	  0
CVX	    2/1/2015	2/2/2015	103.9800034	  2/27/2015	  106.6800003	  1
CVX	    3/1/2015	3/2/2015	106.3199997	  3/31/2015	  104.9800034	  0
CVX	    4/1/2015	4/1/2015	105.7699966	  4/30/2015	  111.0599976	  1
CVX	    5/1/2015	5/1/2015	110.2799988	  5/29/2015	  103	          0
```

In this scenario, 1/2/2015 was the first day of trading in January 2015, and Chevron opened at 111.63 that day. The last day of trading in January 2015 was 1/30/2015, and the stock closed at 102.53 that day. 

Since 102.53 is lower than the open at 111.63, the Growth_period flag = 0.

After this step, the number of growth periods is simply divided by the total number of periods for the share of periods during which the stock price grew, producing this output:

```
Ticker	Growth_period	  Periods   Grow_period_pct	 period_start	period_end	Growth_Interval
CVX	     2	            5	        0.4	           1/1/2015	   5/31/2015	  Month
```

There is no limit on time span, and the code is set up to accommodate days, weeks, months or quarters as the interval

One quirk is that the data won't pull quite right with fewer than two tickers, so to avoid that issue, one must be entered, and it is set to run with the Down Jones industrial average every time.
