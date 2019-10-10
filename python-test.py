##PART-1
#IMPORTING THE LIBRARIES
from nsepy import get_history
from datetime import date
import pandas as pd
import sys
import numpy as np

#STORE DATA WITH DATE AS INDEX
tcs=get_history(symbol='TCS',
                start=date(2015,1,1),
                end=date(2015,12,31))

tcs.insert(0, 'Date',  pd.to_datetime(tcs.index,format='%Y-%m-%d') )
tcs.to_csv('tcs.csv',index=False)
print("TCS DATA STORED")

infy=get_history(symbol='INFY',
                start=date(2015,1,1),
                end=date(2015,12,31))

infy.insert(0, 'Date',  pd.to_datetime(tcs.index,format='%Y-%m-%d') )

infy.to_csv('infy.csv',index=False)
print("INFY DATA STORED")

nifty_it=get_history(symbol='NIFTYIT',
                start=date(2015,1,1),
                end=date(2015,12,31),index=True)

nifty_it.insert(0, 'Date',  pd.to_datetime(tcs.index,format='%Y-%m-%d') )

nifty_it.to_csv('nifty_it.csv',index=False)
print("NIFTY IT  DATA STORED")

#READING DATA
TCS=pd.read_csv('tcs.csv')
INFY=pd.read_csv('infy.csv')
NIFTY=pd.read_csv('nifty_it.csv')

print(TCS['Close'])
#CREATING A LIST OF TOTAL STOCKS
total_stocks=[TCS,INFY,NIFTY]

#INDEXING USING DATE
def indexing(stock):
    stock['Date']=pd.to_datetime(stock['Date'])
    stock.index = stock['Date']
    return stock
for i in total_stocks:
    indexing(i)

#CALCULATE MOVING AVERAGES FOR WEEK
week=[4,16,28,40,52]    
def calculate_moving_average(stock,week=[4,16,28,40,52]):
    df=pd.DataFrame()
    df['Close'] = stock['Close'].resample('W').mean()
    df['Close']=stock['Close']
    for i in range(len(week)):
        moving_avg=df['Close'].rolling(week[i]).mean()
        if week[i]==52:
            stock['52_WEEK']=moving_avg
        df['M.A.']=moving_avg
        print('Moving Averages: for {0} weeks: \n\n {1}' .format(week[i], df['Close']))

for i in total_stocks:
    if i.empty:
        print("STOCK LIST IS EMPTY")
    else: 
        calculate_moving_average(i)
#ROLLING WINDOW FOR SIZE 10 AND 75
#FIRST WE HAVE TO CONSIDER STOCK HOLIDAYS i.e SATURDAYS AND SUNDAYS ,closing price of fridays should be forwarded
TCS_NEW=TCS.asfreq(freq='D',method='pad')
INFY_NEW=INFY.asfreq(freq='D',method='pad')
NIFTY_NEW=NIFTY.asfreq(freq='D',method='pad')
total_stocks_new=[TCS_NEW,INFY_NEW,NIFTY_NEW]

def window_size_10_75(stock,week=[10,75]):
    df=pd.DataFrame()
    df['Close']=stock['Close']
    for i in range(len(week)):
        moving_avg=df['Close'].rolling(week[i]).mean()
        df['M.A.']=moving_avg
        print('Moving Averages: for {0} weeks: \n\n {1}' .format(week[i], df['Close']))
        
for i in total_stocks_new:
    if i.empty:
        print("STOCK LIST IS EMPTY")
    else:
        window_size_10_75(i)

#VOLUME SHOCK
TCS['next_vol_col']=TCS.Volume.shift(1)
TCS['VOL_SHOCK']=((abs(TCS['next_vol_col']-TCS['Volume'])/TCS['Volume']*100)>10).astype(int)
print(TCS.head())

INFY['next_vol_col']=INFY.Volume.shift(1)
INFY['VOL_SHOCK']=((abs(INFY['next_vol_col']-INFY['Volume'])/INFY['Volume']*100)>10).astype(int)

NIFTY['next_vol_col']=NIFTY.Volume.shift(1)
NIFTY['VOL_SHOCK']=((abs(NIFTY['next_vol_col']-NIFTY['Volume'])/NIFTY['Volume']*100)>10).astype(int)

#VOLUME SHOCK DIRECTION
def vol_shock_direction(stock):
    if stock['VOL_SHOCK']==0:
        pass
    else:
        if stock['next_vol_col']-stock['Volume']<0:
            return 0
        else:
            return 1

TCS['VOL_SHOCK_DIR']=99999
TCS['VOL_SHOCK_DIR']=TCS.apply(vol_shock_direction,axis=1)

INFY['VOL_SHOCK_DIR']=99999
INFY['VOL_SHOCK_DIR']=INFY.apply(vol_shock_direction,axis=1)

NIFTY['VOL_SHOCK_DIR']=99999
NIFTY['VOL_SHOCK_DIR']=NIFTY.apply(vol_shock_direction,axis=1)

#SINCE PRICE SHOCK AND BLACK SWAN HAS SAME CONDITION PRICE SHOCK VALUE AND PRICING BLACK SWAN HAS SAME VALUE
#PRICE SHOCK AND PRICING BLACK SWAN 
TCS['next_price_col']=TCS.Close.shift(1)
TCS['PRICE_SHOCK']=((abs(TCS['next_price_col']-TCS['Close'])/TCS['Close']*100)>2).astype(int)
TCS['PRICING_BLACK_SWAN']=TCS['PRICE_SHOCK']
print(TCS.head())

INFY['next_price_col']=INFY.Close.shift(1)
INFY['PRICE_SHOCK']=((abs(INFY['next_price_col']-INFY['Close'])/INFY['Close']*100)>2).astype(int)
INFY['PRICING_BLACK_SWAN']=INFY['PRICE_SHOCK']

NIFTY['next_price_col']=NIFTY.Close.shift(1)
NIFTY['PRICE_SHOCK']=((abs(NIFTY['next_price_col']-NIFTY['Close'])/NIFTY['Close']*100)>2).astype(int)
NIFTY['PRICING_BLACK_SWAN']=NIFTY['PRICE_SHOCK']

#PRICE SHOCK DIRECTION
def price_shock_direction(stock):
    if stock['PRICE_SHOCK']==0:
        pass
    else:
        if stock['next_price_col']-stock['Close']<0:
            return 0
        else:
            return 1

TCS['PRICE_SHOCK_DIR']=99999
TCS['PRICE_SHOCK_DIR']=TCS.apply(price_shock_direction,axis=1)
TCS['PRICING_BLACK_SWAN_DIR']=TCS['PRICE_SHOCK_DIR']

INFY['PRICE_SHOCK_DIR']=99999
INFY['PRICE_SHOCK_DIR']=INFY.apply(price_shock_direction,axis=1)
INFY['PRICING_BLACK_SWAN_DIR']=INFY['PRICE_SHOCK_DIR']

NIFTY['PRICE_SHOCK_DIR']=99999
NIFTY['PRICE_SHOCK_DIR']=NIFTY.apply(price_shock_direction,axis=1)
NIFTY['PRICING_BLACK_SWAN_DIR']=NIFTY['PRICE_SHOCK_DIR']

#PRICE SHOCK WITHOUT NO VOLUME SHOCK
TCS['no_vol_shock']=(~(TCS['VOL_SHOCK'].astype(bool))).astype(int)
TCS['PRICE_SHOCK_W/O_VOL_SHOCK']=TCS['no_vol_shock']& TCS['PRICE_SHOCK']
print(TCS.head(5))

INFY['no_vol_shock']=(~(INFY['VOL_SHOCK'].astype(bool))).astype(int)
INFY['PRICE_SHOCK_W/O_VOL_SHOCK']=INFY['no_vol_shock']& INFY['PRICE_SHOCK']

NIFTY['no_vol_shock']=(~(NIFTY['VOL_SHOCK'].astype(bool))).astype(int)
NIFTY['PRICE_SHOCK_W/O_VOL_SHOCK']=NIFTY['no_vol_shock']& NIFTY['PRICE_SHOCK']

####PART-2
from bokeh.plotting import figure
from bokeh.io import show
from statsmodels.tsa.stattools import pacf
def draw_timeseries(stock):
    graph = figure(x_axis_type="datetime", title="Time Series Graph of Prices", plot_height=500, plot_width=1000)
    graph.xgrid.grid_line_color=None
    graph.ygrid.grid_line_alpha=0.5
    graph.xaxis.axis_label = 'Date'
    graph.yaxis.axis_label = 'Price'
    #for i in range(len(stock['VOL_SHOCK'])-1):
     #   if stock['VOL_SHOCK'][i]!=stock['VOL_SHOCK'][i+1]:
      #      graph.line(TCS['Date'], TCS['Close'],line_color='blue')
       # elif stock['VOL_SHOCK'][i]==stock['VOL_SHOCK'][i+1]:
        #    graph.line(TCS['Date'], TCS['Close'],line_color='red')
    graph.line(TCS['Date'], TCS['Close'],line_color='blue')
    graph.circle(TCS.index, TCS.Close*TCS["PRICE_SHOCK_W/O_VOL_SHOCK"], size=5, legend='price shock without vol shock',color='green')
    show(graph)

draw_timeseries(TCS)
draw_timeseries(INFY)
draw_timeseries(NIFTY)

def draw_pacf(stock):
    lags=50
    x=list(range(lags))
    graph = figure(plot_height=500, title="Pacf PLot")
    partial_autocorr = pacf(stock["Close"],nlags=lags)
    graph.vbar(x=x,top=partial_autocorr, width=0.9)
    show(graph)
draw_pacf(TCS)
draw_pacf(INFY)
draw_pacf(NIFTY)

##Gradient Color
from bokeh.models import ColumnDataSource, LinearColorMapper
p= figure()
x=TCS['52_WEEK']
y=list(range(len(x)))
data_source = ColumnDataSource({'x':TCS['52_WEEK'],'y':TCS['Date']})
color_mapper = LinearColorMapper(palette='Blues8', low=min(y), high=max(y))

# specify that we want to map the colors to the y values, 
# this could be replaced with a list of colors
p.scatter(x,y,color={'field': 'y', 'transform': color_mapper})

show(p)
