import backtrader as bt
import backtrader.indicators as btind
from datetime import datetime
from collections import defaultdict
from utils import RegisterModel


# Create a new strategy
@RegisterModel.on
class MultiRSIStrategy(bt.Strategy):
    def __init__(self):
        # Create an RSI indicator
        
        # make multiple indicator for multiple asset  
        self.inds = defaultdict(dict)
        for d in self.datas:
            self.inds[d]['rsi'] = bt.indicators.RSI()

        self.order_track_list = []
        


    def next(self):
        # Access the RSI indicator's value

       # for every stock in my data
        for d in self.datas:
            # for rsi value 
            rsi_value = self.inds[d]['rsi'].get()[0]
            pos = self.getposition(d).size

            print(f'position on {d._name}: {pos}')
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
        dt = self.datas[0].datetime.date(0)

        if order.status in [order.Completed]:
            if order.isbuy():
                op_name = 'BUY'
            elif order.issell():
                op_name = 'SELL'

            self.order_track_list.append(f"""{dt}: {op_name} , {order.data._name}
                    價格: {round(order.executed.price, 2)} 
                    成本: {round(order.executed.value, 2)} 
                    手續費: {round(order.executed.comm, 2)}
                    Cash: {round(self.broker.cash, 2)}
                    Asset Value: {round(self.broker.getvalue(), 2)}
                    {self.position}""")
            self.bar_executed = len(self)
                
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            print("訂單取消/餘額不足/拒絕交易")

    
    def notify_trade(self, trade):
        # trade object no attri isclose
        if not trade.isclosed:
            return
        print("交易收益：毛利 %.2f 淨利：%.2f" % (trade.pnl, trade.pnlcomm))

