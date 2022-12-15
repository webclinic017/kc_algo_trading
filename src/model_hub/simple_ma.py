import backtrader as bt
import backtrader.indicators as btind
from datetime import datetime
from collections import defaultdict
from utils import RegisterModel
import numpy as np 

# Create the strategy
class TheStrategy(bt.Strategy):
    def __init__(self):
        # Set the moving average periods
        self.maperiod_fast = 12
        self.maperiod_slow = 26

        # Create the MACD indicator
        self.macd = btind.MACD(self.data,
                               fastperiod=self.maperiod_fast,
                               slowperiod=self.maperiod_slow)

    def next(self):
        # Check if the MACD line crosses above the signal line
        if self.macd.macd[0] > self.macd.signal[0] and self.macd.macd[-1] < self.macd.signal[-1]:
            # Buy the asset
            self.buy()

        # Check if the MACD line crosses below the signal line
        elif self.macd.macd[0] < self.macd.signal[0] and self.macd.macd[-1] > self.macd.signal[-1]:
            # Sell the asset
            self.sell()


# Notice the trading strategy should decouple with order/observer and analyzer
@RegisterModel.on
class MaCrossover(bt.Strategy): 
    # Moving average parameters
    params = (
        ("pfast", 7),  # period for the fast moving average
        ("pslow",20)   # period for the slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            self.log('ORDER ACCEPTED/SUBMITTED', dt=order.created.dt)
            self.order = order
            return

        if order.status in [order.Expired]:
            self.log('BUY EXPIRED')

        elif order.status in [order.Completed]:
            
            # below sometimes the cost will be negative
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

        # Sentinel to None: new orders allowed
        self.order = None

    def log(self, txt, dt=None):
        dt = self.datas[0].datetime.date(0)
        print(dt,':' ,txt)        

    def next(self):
        op_price = self.data.close[0]

        #print(self.data) # this is a object 
        # print('--Next')
        # print(f'{self.datas[0].datetime.date(0)}')
        # print(self.data.close[0]) # this is the line with 
        # print(self.data.close[-1])

        if self.position:
            position_price = self.position.price
            dt = self.datas[0].datetime

            print(dt, ' position price:',position_price)

        if self.crossover > 0:  # if fast crosses slow to the upside
            print("close short position")
            self.close() # clos short position 
            print(self.position)
            self.buy() # enter long
            print(f"Buy at prices {op_price}")
            print(self.position)
                
        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()# close long position
            print(f"close long position")
            print(self.position)
            self.sell()
            print("Sale shares at prices {}".format(self.data.close[0]))
            print(self.position)


@RegisterModel.on
class EnhanceRsi(bt.Strategy):

    # specify the param for optimizer
    params = dict(
        pfast=7,  # period for the fast moving average
        pslow=20,  # period for the slow moving average
        rsi_period=5, 
    )

    def __init__(self):
        # Create an RSI indicator
        # make multiple indicator for multiple asset  
        self.inds = defaultdict(dict)

        # Need to apply the inde to all the 
        for d in self.datas:
            self.inds[d]['f_sma'] = bt.talib.SMA(self.data, timeperiod=self.p.pfast)
            self.inds[d]['rsi'] = bt.indicators.RSI()
            #self.inds[d]['f_sma'] = bt.ind.SMA(period=self.p.pfast)  # fast moving average
            self.inds[d]['w_sma'] = bt.ind.SMA(period=self.p.pslow)  # fast moving average
            self.inds[d]['crossover'] = bt.ind.CrossOver(
                self.inds[d]['f_sma'], self.inds[d]['w_sma']) 

        # the model is actually sit in Indicator 
        # even if you have suctomized data -> you will need indicator to also support it


    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        dt = self.datas[0].datetime.date(0)

        if order.status in [order.Completed]:
            if order.isbuy():
                op_name = 'BUY'
            elif order.issell():
                op_name = 'SELL'
            # print(f"""{dt}: {op_name} , {order.data._name}
            #         價格: {round(order.executed.price, 2)} 
            #         成本: {round(order.executed.value, 2)} 
            #         手續費: {round(order.executed.comm, 2)}
            #         Cash: {round(self.broker.cash, 2)}
            #         Asset Value: {round(self.broker.getvalue(), 2)}
            #         {self.position}
            #        """)
            self.bar_executed = len(self)

    def next(self):
        
        # it seems 
        # for i, d in enumerate(d for d in self.datas if len(d)):
        #     if not self.order[d._name]:
        #         continue

        current_po_size = self.position.size
        current_cash = self.broker.cash 
       # for every stock in my data
        for d in self.datas:
            # for rsi value 
            rsi_value = self.inds[d]['rsi'].get()[0]

            # Buy & Sell 
            for i in range(21):
                crossover = self.inds[d]['crossover'][-i]
                if crossover < 0 and rsi_value < 35:
                    # if cur size < 0, it is a signal to cover-call
                    if current_po_size < 0 :
                        self.close()
                    else:
                        self.buy(d)
                if crossover > 0 and rsi_value > 65:
                    if current_po_size > 0 :
                        self.close()
                    else:
                        self.sell(d)

            #----- for short position, we need a cover call for some cases
            cur_open_position_value = current_po_size * d.close[0]
            if cur_open_position_value < 0:
                if abs(cur_open_position_value)> (0.8 * current_cash):
                    self.close(size=int(0.5*self.position.size))

# Create a new strategy
@RegisterModel.on
class RsiStrategy(bt.Strategy):
    def __init__(self):
        # Create an RSI indicator
        
        # make multiple indicator for multiple asset  
        self.inds = defaultdict(dict)
        for d in self.datas:
            self.inds[d]['rsi'] = bt.indicators.RSI()


    def next(self):
        # Access the RSI indicator's value

       # for every stock in my data
        for d in self.datas:
            # for rsi value 
            rsi_value = self.inds[d]['rsi'].get()[0]

            # Use the RSI value in your strategy logic

            if rsi_value < 30:
                # RSI is oversold, buy
                self.buy(d)
            elif rsi_value > 70:
                # RSI is overbought, sell
                self.sell(d) 

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        dt = self.datas[0].datetime.now()

        if order.status in [order.Completed]:
            if order.isbuy():
                op_name = 'BUY'
            elif order.issell():
                op_name = 'SELL'
            print(f"""{dt}: {op_name} , {order.data._name}
                    價格: {round(order.executed.price, 2)} 
                    成本: {round(order.executed.value, 2)} 
                    手續費: {round(order.executed.comm, 2)}
                    Cash: {round(self.broker.cash, 2)}
                    Asset Value: {round(self.broker.getvalue(), 2)}
                    {self.position}
                   """)
            self.bar_executed = len(self)
                
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            print("訂單取消/餘額不足/拒絕交易")

    
    def notify_trade(self, trade):
        # trade object no attri isclose
        if not trade.isclosed:
            return

        print("交易收益：毛利 %.2f 淨利：%.2f" % (trade.pnl, trade.pnlcomm))


class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=7,  # period for the fast moving average
        pslow=20   # period for the slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
       
        if self.crossover > 0:  # if fast crosses slow to the upside
        
            #self.close()
            #print(self.position)
            self.buy() # enter long
            print('!!', self.sizer)
            print("Buy {} shares".format( self.data.close[0]))
            print(self.position)
                
 
        elif self.crossover < 0:  # in the market & cross to the downside
            print('Close long position')
            self.close()# close long position
            print(self.position)
            self.sell()
            print("Sale {} shares".format(self.data.close[0]))
            print(self.position)