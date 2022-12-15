import yfinance as yf
import backtrader as bt
from data_pipe.td_price_history import HistoryPriceDataHandler


#https://community.backtrader.com/topic/3979/help-with-yahoofinance-data/2
# according to some thread the bt.feed-yahoo is dead
# Create an instance of the backtesting engine


def get_stock_data(stock_name: str, period_start:str='2022-01-01', period_end:str='2023-01-01'):
    """_summary_

    Args:
        stock_name (str): _description_
        period_start (str): _description_
        period_end (str): _description_
    """
    return bt.feeds.PandasData(
        dataname=yf.download(stock_name, period_start, period_end))

def get_stock_data_td(symbol, frequency=5, frequency_type='minute', start_dt='2022-06-01'):

    db_op = HistoryPriceDataHandler()
    res_df = db_op.read_hist_table(symbol=symbol, 
        frequency=frequency,
        frequency_type=frequency_type, start_dt=start_dt)

    return bt.feeds.PandasData(
        dataname=res_df)   
# ideally we need a data-pipe that include all the data
# so we are not only do technical analysis on price/volume ...etc 
# we can also do sentiment analysis and ... other analysis