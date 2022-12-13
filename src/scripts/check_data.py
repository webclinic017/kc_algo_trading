import sys 
sys.path.append('./')
from data_pipe.stock_feeder import get_stock_data

data = get_stock_data('RIOT')


# this is a object of feeds.pandafeed.PandasData object