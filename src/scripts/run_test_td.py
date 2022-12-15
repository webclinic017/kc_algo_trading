
import argparse
import sys
sys.path.append('./')
# regist model to RegisterModel
import backtrader as bt
from model_hub import simple_ma
from data_pipe.stock_feeder import get_stock_data, get_stock_data_td
from analyzer_hub.cash_market import CashMarket
from utils import RegisterModel
# from observer_hub.simple import MyObserver, MyObserver2
import pandas as pd

def parse_args(pargs=None):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=(
            'Multiple Values and Brackets'
        )
    )
    parser.add_argument('--stock', required=False, default='RIOT',
                        metavar='kwargs', help='kwargs in key=value format')

    parser.add_argument('--model', required=False, default='RSIStrategy', 
                       help='run show_register_model.py')

    parser.add_argument('--plot', required=False, default='',
                        nargs='?', const='{}',
                        metavar='kwargs', help='kwargs in key=value format')

    return parser.parse_args(pargs)


def main():
    args = parse_args()

    cerebro = bt.Cerebro()
    # Create an instance of the strategy
    # Add the strategy and data to the engine
    # need to pash the class. .. 
    
    # 
    cerebro.addstrategy(RegisterModel(args.model))


    # from collections.abc, by using py3.10, which is 3.9 above
    # you will hit the problem of AttributeError: module 'collections' has no attribute 'Iterable'
    # which is similar to this problem: https://github.com/nerdocs/pydifact/issues/46
    # from collections.abc
    # == code
    # strats = cerebro.optstrategy(
    #         RegisterModel(args.model),
    #         pfast = range(1, 11), 
    #         pslow = range(20, 50, 5))
 

 
    stock_name = args.stock
    data = get_stock_data_td(symbol=stock_name)
    # add name so we can hook in Strategy
    cerebro.adddata(data, name=stock_name)

    # you can add analyzers and it will be capture in result 
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name = 'SR', 
    timeframe=bt.TimeFrame.Months)

    cerebro.addanalyzer(bt.analyzers.DrawDown, _name = 'DW')
    cerebro.addanalyzer(bt.analyzers.TimeReturn, _name = 'TR', 
                        timeframe=bt.TimeFrame.Months)
                        
    cerebro.addanalyzer(bt.analyzers.Returns, _name = "returns")

    cerebro.addanalyzer(CashMarket, _name = "cash_market")


    # Set the starting cash
    cash = 100000
    cerebro.broker.setcash(cash)

    # add size to all strategy 
    cerebro.addsizer(bt.sizers.SizerFix, stake=30)

    #cerebro.addsizer(bt.sizers.PercentSizer, percents = 10)

    # the sizer can be specified with particular strategy
    # ---
    # idx = cerebro.addstrategy(MyStrategy, myparam=myvalue)
    # cerebro.addsizer_byidx(idx, bt.sizers.SizerFix, stake=5)
    # -- 

    # Run the backtest
    result = cerebro.run()

    # Dictionary
    res, cols = result[0].analyzers.getbyname("cash_market").get_analysis()
    print(pd.DataFrame(res, columns=cols))
    # p.a Sharpe Ration 
    print('Sharpe Ratio:', result[0].analyzers.SR.get_analysis())

    print('Max DrawDown:', result[0].analyzers.DW.get_analysis().max)

    # monthly gain 
    # for date, value in  result[0].analyzers.TR.get_analysis().items():
    #     print(date.date(), f'monthly gain:{round(cash*value, 2)}$', f' {round(value*100, 4)}%:')  

    # # suggest by chatgpt
    if args.plot:
        cerebro.plot()

if __name__ == '__main__':
    main() 