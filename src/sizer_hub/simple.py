import backtrader as bt
import math 

# the operational size would be related to risk/uncertainty 
# in complex trading strategy we might need to take care of it
# 計算交易部位
class sizer(bt.Sizer):
    def _getsizing(self, comminfo, cash, data, isbuy):
        if isbuy:
            return math.floor(cash/data[1])
        else:
            return self.broker.getposition(data)