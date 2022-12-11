
import backtrader as bt
import yfinance as yf

from datetime import datetime
import sys
sys.path.append('./')
from model_hub.simple_ma import TheStrategy, MAcrossover, SmaCross
from data_pipe.stock_feeder import get_stock_data
from analyzer_hub.cash_market import CashMarket

import pandas as pd



cerebro = bt.Cerebro()
# Create an instance of the strategy
# Add the strategy and data to the engine
# need to pash the class. .. 
cerebro.addstrategy(MAcrossover)


stock_list = [
    #'TSLA',
 #'RIOT',
 'MSFT',
 # 'LRCX'
]

for stock_name in stock_list:
    data = get_stock_data(stock_name=stock_name)
    cerebro.adddata(data)

# you can add analyzers and it will be capture in result 
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name = 'SR', 
timeframe=bt.TimeFrame.Months)

cerebro.addanalyzer(bt.analyzers.DrawDown, _name = 'DW')
cerebro.addanalyzer(bt.analyzers.TimeReturn, _name = 'TR', 
                     timeframe=bt.TimeFrame.Months)

cerebro.addanalyzer(CashMarket, _name = "cash_market")



# Set the starting cash
cash = 100000
cerebro.broker.setcash(cash)

# add size to all strategy 
cerebro.addsizer(bt.sizers.SizerFix, stake=20)  # default sizer for strategies

# the sizer can be specified with particular strategy
# ---
# idx = cerebro.addstrategy(MyStrategy, myparam=myvalue)
# cerebro.addsizer_byidx(idx, bt.sizers.SizerFix, stake=5)
# -- 

# Run the backtest
result = cerebro.run()

# Dictionary
res, cols = result[0].analyzers.getbyname("cash_market").get_analysis()
print('-----------')
print(pd.DataFrame(res, columns=cols))
print('----------------')
print('Sharpe Ratio:', result[0].analyzers.SR.get_analysis())
print('Max DrawDown:', result[0].analyzers.DW.get_analysis().max)
for date, value in  result[0].analyzers.TR.get_analysis().items():
     print(date.date(), f'gain:{round(cash*value, 2)}$', f'gain {round(value*100, 4)}%:')  

# # suggest by chatgpt
# cerebro.plot()