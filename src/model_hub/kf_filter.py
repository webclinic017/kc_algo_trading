import backtrader as bt
import numpy as np
import datetime

# Kalman Pair Trade with EWA/EWC (from Ernie Chan's "Algorithmic Trading")
# This strategy is from Ernie Chan's Algorithmic Trading, implemented using backtrader.
# Code src: https://community.backtrader.com/topic/1512/kalman-pair-trade-with-ewa-ewc-from-ernie-chan-s-algorithmic-trading
# reading ref : https://medium.com/analytics-vidhya/understanding-and-implementing-kalman-filter-in-python-for-pairs-trading-9b8986d79b2d
class KalmanPair(bt.Strategy):
    """In pairs trading, we should look for a “stationary” correlation 
    between two assets and trade when the prices move away from the mean correlation.
    If we take Ernest Chan’s pairs trading example using the ETF’s EWA and EWC, 
    from 2006 to 2012, we can see that, the prices are correlated (Figure 3a) 
    and performing a linear regression between EWC and EWA, 
    we find slope=0.9624 and intercept=6.4113 


    Args:
        bt (_type_): _description_
    """
    params = (("printlog", False), ("quantity", 1000))

    def log(self, txt, dt=None, doprint=False):
        """Logging function for strategy"""
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print(f"{dt.isoformat()}, {txt}")

    def __init__(self):
        self.delta = 0.0001
        self.Vw = self.delta / (1 - self.delta) * np.eye(2)
        self.Ve = 0.001

        self.beta = np.zeros(2)
        self.P = np.zeros((2, 2))
        self.R = np.zeros((2, 2))

        self.position_type = None  # long or short
        self.quantity = self.params.quantity

    def next(self):

        x = np.asarray([self.data0[0], 1.0]).reshape((1, 2))
        y = self.data1[0]

        self.R = self.P + self.Vw  # state covariance prediction
        yhat = x.dot(self.beta)  # measurement prediction

        Q = x.dot(self.R).dot(x.T) + self.Ve  # measurement variance

        e = y - yhat  # measurement prediction error

        K = self.R.dot(x.T) / Q  # Kalman gain

        self.beta += K.flatten() * e  # State update
        self.P = self.R - K * x.dot(self.R)

        sqrt_Q = np.sqrt(Q)

        if self.position:
            if self.position_type == "long" and e > -sqrt_Q:
                self.close(self.data0)
                self.close(self.data1)
                self.position_type = None
            if self.position_type == "short" and e < sqrt_Q:
                self.close(self.data0)
                self.close(self.data1)
                self.position_type = None

        else:
            if e < -sqrt_Q:
                self.sell(data=self.data0, size=(self.quantity * self.beta[0]))
                self.buy(data=self.data1, size=self.quantity)

                self.position_type = "long"
            if e > sqrt_Q:
                self.buy(data=self.data0, size=(self.quantity * self.beta[0]))
                self.sell(data=self.data1, size=self.quantity)
                self.position_type = "short"

        self.log(f"beta: {self.beta[0]}, alpha: {self.beta[1]}")


def run():
    cerebro = bt.Cerebro()
    cerebro.addstrategy(KalmanPair)

    startdate = datetime.datetime(2007, 1, 1)
    enddate = datetime.datetime(2017, 1, 1)

    ewa = bt.feeds.YahooFinanceData(dataname="EWA", fromdate=startdate, todate=enddate)
    ewc = bt.feeds.YahooFinanceData(dataname="EWC", fromdate=startdate, todate=enddate)

    cerebro.adddata(ewa)
    cerebro.adddata(ewc)
    # cerebro.broker.setcommission(commission=0.0001)
    cerebro.broker.setcash(100_000.0)

    print(f"Starting Portfolio Value: {cerebro.broker.getvalue():.2f}")
    cerebro.run()
    print(f"Final Portfolio Value: {cerebro.broker.getvalue():.2f}")
    cerebro.plot()