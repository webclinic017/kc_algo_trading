import backtrader as bt
from collections import defaultdict

# Create the observer class
class MyObserver(bt.Observer):
    def next(self):
        # Print the details of all executed buy orders
        for order in self.buy_orders:
            print("**Buy order:", order)

        # Print the details of all executed sell orders
        for order in self.sell_orders:
            print("**Sell order:", order)

class MyObserver2(bt.Observer):
    def __init__(self):
        self.trades = defaultdict(list)

    def next(self):
        for order in self.orders:
            if order.isbuy():
                self.trades[order.data].append((order.executed.price, order.executed.size))
            elif order.issell():
                self.trades[order.data].append((order.executed.price, -order.executed.size))