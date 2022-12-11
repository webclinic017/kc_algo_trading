import backtrader as bt
import backtrader.indicators as btind
from datetime import datetime
 
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

class MAcrossover(bt.Strategy): 
    # Moving average parameters
    params = (('pfast',20),('pslow',50),)

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}') # Comment this line when running optimization

    def __init__(self):
        self.dataclose = self.datas[0].close

		# Order variable will contain ongoing order details/status
        self.order = None

        # Instantiate moving averages
        self.slow_sma = bt.indicators.MovingAverageSimple(self.datas[0], 
                        period=self.params.pslow)
        self.fast_sma = bt.indicators.MovingAverageSimple(self.datas[0], 
                        period=self.params.pfast)

        self.crossover = bt.ind.CrossOver(self.fast_sma, self.slow_sma)  # crossover signal

    def next(self):
        op_price = self.data.close[0]


        #print(self.data) # this is a object 
        print('print self data datetime')
        print(self.data.datetime)
        print('-- presee enter to continoue')
        input()
        if self.crossover > 0:  # if fast crosses slow to the upside
            print(f"close short position")
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