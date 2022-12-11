import yfinance as yf
import backtrader as bt


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


# ideally we need a data-pipe that include all the data
# so we are not only do technical analysis on price/volume ...etc 
# we can also do sentiment analysis and ... other analysis