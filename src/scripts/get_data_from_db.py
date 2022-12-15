import sys 
sys.path.append('./')
from data_pipe.td_price_history import HistoryPriceDataHandler
import pandas as pd 
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description='Get Data from Historical Table')
    parser.add_argument('--symbol', required=True, type=str)
    parser.add_argument('--frequency_type', '-ft',  default='minute', type=str)
    parser.add_argument('--frequency', '-f',  default=5, type=int)
    return parser.parse_args()

def main():
    param = parse_args()
    db_op = HistoryPriceDataHandler()
    res_df = db_op.read_hist_table(symbol=param.symbol, 
        frequency=param.frequency,
        frequency_type=param.frequency_type)

    print(res_df.head())


    table_name = db_op.get_hist_table_name(symbol=param.symbol, 
        frequency=param.frequency,
        frequency_type=param.frequency_type)
    db_op._clean_df(table_name)


if __name__ == '__main__':
    main()