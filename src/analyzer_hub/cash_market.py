
import backtrader as bt

# adding a customized analyzer to save all output into list 
class CashMarket(bt.analyzers.Analyzer):
    """
    Analyzer returning cash and market values
    currently only support singe instrument 
    """

    def create_analysis(self):
        self.rets = []
        self.vals = 0.0

    def notify_cashvalue(self, cash, value):
        """it overwrite the parent functions

        Args:
            cash (float): the cash on hand
            value (float): the total asset value 
        """
        # the self.strategy is the design from bt
        close_price = self.datas[0].close[0]
        row_value = (self.strategy.datetime.datetime().strftime("%Y-%m-%d"), 
            int(cash), int(value), int( self.strategy.position.size), close_price)
        
        self.rets.append(row_value)
        # position = self.strategy.position.size


    def get_analysis(self):
        cols =  ('date', 'cash', 'value', 'open_size', 'close_price')
        return self.rets, cols