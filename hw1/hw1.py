import numpy as np

import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd




def simulate(start,end,stocks,allocations):
	
	dt_timeofday = dt.timedelta(hours=16) #closing price
	ldt_timestamps = du.getNYSEdays(start, end, dt_timeofday) #get closing times
	c_dataobj = da.DataAccess('Yahoo')#,cachestalltime=0)
	ls_keys = ['close','actual_close']
	ldf_data = c_dataobj.get_data(ldt_timestamps, stocks, ls_keys)
	d_data = dict(zip(ls_keys, ldf_data))
	
	
	#get close price and calculate daily return
	na_price = d_data['close'].values
	na_normalized_price = na_price / na_price[0, :] #normalize values
	#print na_normalized_price
	tradingDays = na_price.shape[0] #usually 252
	numStocks=len(stocks)
	
	#normalized
	na_rets = na_normalized_price.copy() #get a copy because returnize is INPlace
	
	#get the WEIGHTED (ACCORDING TO ALLOCATION) sum of daily returns for all stocks to get portfolio return
	weighted_rets=na_normalized_price.copy()
	for i in range(0,numStocks):
		weighted_rets[:,i]=weighted_rets[:,i]*allocations[i]
	
	portfolio_rets=np.sum(weighted_rets,1) ##shrink the columns(stocks) into one(1==2, zero baed) - summing
	#print portfolio_rets.shape
	#print "fund return "+str(portfolio_rets.shape)
	#print portfolio_rets
	
	
	daily_ret=np.zeros(tradingDays)
	for i in range(1,tradingDays):
		daily_ret[i]=portfolio_rets[i]/portfolio_rets[i-1]-1.0
	#print daily_ret
	
	vol=np.std	(daily_ret); #Volatility (stdev of daily returns)
	avg_daily_ret=np.mean(daily_ret,0)
	#print "vol = "+str(vol)+ " mean: "+str(avg_daily_ret)
	
	
	#sharpe ratio - 252 trading days
	#Sharpe ratio (Always assume you have 252 trading days in an year. And risk free rate = 0) of the total portfolio
	sharpe=np.sqrt(tradingDays)*avg_daily_ret/vol
	#print "sharpe "+str(sharpe)
	#cumulative_return is the last value in the weighted sum for portfolio_return
	cum_ret=portfolio_rets[tradingDays-1]
	#print "cumulative Return "+str(cum_ret)

	return vol,avg_daily_ret,sharpe,cum_ret




#goal function
startdate=dt.datetime(2011,1,1)
enddate=dt.datetime(2011,12,31)
#vol, daily_ret, sharpe, cum_ret = simulate(startdate, enddate, ['GOOG','AAPL','GLD','XOM'], [0.2,0.3,0.4,0.1])
response=simulate(startdate, enddate, ['AAPL','GLD','GOOG','XOM'], [0.4,0.4,0.0,0.2])
print str(response)+"\n----------\n"

startdate=dt.datetime(2010,1,1)
enddate=dt.datetime(2010,12,31)
#vol, daily_ret, sharpe, cum_ret = simulate(startdate, enddate, ['GOOG','AAPL','GLD','XOM'], [0.2,0.3,0.4,0.1])
response=simulate(startdate, enddate, ['AXP','HPQ','IBM','HNZ'], [0.0,0.0,0.0,1.0])
print str(response)+"\n----------\n\n\n"


#HW1 Part3, portfolio optimizer
startdate=dt.datetime(2011,1,1)
enddate=dt.datetime(2011,12,31)
highestSharpe=0.0

#print np.arange(0.0,1.1,0.1)
for i in np.arange(0.0,1.1,0.1):
	for j in np.arange(0.0,1.1,0.1):
		for q in np.arange(0.0,1.1,0.1):
			for k in np.arange(0.0,1.1,0.1):
				#print str(i)+","+str(j)+","+str(q)+","+str(k)
				if((i+j+q+k)==1.0):
					response=simulate(startdate, enddate, ['BRCM', 'ADBE', 'AMD', 'ADI'], [i,j,q,k])
					#print "sharpe: "+str(response[2])
					if(response[2]>highestSharpe):
						highestSharpe=response[2]
						print "i,j,q,k "+str(i)+","+str(j)+","+str(q)+","+str(k)
print "highestSharpe: "+str(highestSharpe)



















