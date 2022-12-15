import sys 
sys.path.append('./')
from td.credentials import TdCredentials
from td.client import TdAmeritradeClient
from data_pipe.td_price_history import HistoryPriceDataHandler
from datetime import datetime 
import pandas as pd 
import argparse
import time 


# 
# you need to get the client_id from td-web

def parse_args():
    parser = argparse.ArgumentParser(description='Set Up Historical Data')

    parser.add_argument('--cid', required=True, type=str,
                        help='client-id in app from TD dev account')

    parser.add_argument('--redirect_uri', default="http://localhost", 
        type=str,help='redirect_uri from TD dev account')

    parser.add_argument('--td_cred_path', 
                        default='../td_credentails.json',
                        help='Plot using numfigs figures')

    return parser.parse_args()

def get_td_client():
    param = parse_args()

    # Intialize our `Credentials` object.
    td_credentials = TdCredentials(
        client_id=param.cid,
        redirect_uri=param.redirect_uri,
        credential_file=param.td_cred_path,  
        # first time you dont have cretail file, 
        # it will pop out a window
    )

    # Initalize the `TdAmeritradeClient`
    td_client = TdAmeritradeClient(
        credentials=td_credentials
    )

    return td_client

def main():
    td_client = get_td_client()

    stock_list = ["AAPL", "LRCX", "RIOT", "AMD", "KLAC"]
    for symbol in stock_list:
        get_price_history(td_client=td_client, symbol=symbol)
        time.sleep(3)



def get_price_history(td_client, symbol):
    """

    Args:
        td_client (TdAmeritradeClient): the object for api
        symbol (str): the name of stock
    """

    # symbol = 'MSFT'
    start_date = str(datetime.today().date())
    frequency_type = 'minute'
    frequency = 5
    period = 3


    # if you specify a start_date with period
    # it somehow get more data to u 

    price_history_service = td_client.price_history()
    
    price_history = price_history_service.get_price_history(
                    symbol=symbol,
                    frequency_type=frequency_type,
                    frequency=frequency,
                    start_date = datetime.strptime(start_date, '%Y-%M-%d'), 
                    #end_date=datetime.strptime(end_date, '%Y-%M-%d'), 
                    period_type='day',
                    period=period,
                    extended_hours_needed=False)


    df = pd.DataFrame(price_history['candles'])
    if len(df)==0:
        print(f'skip empty table {symbol}')
        return 
    db_ops = HistoryPriceDataHandler()
    table_name= db_ops.get_hist_table_name(symbol, frequency_type, frequency)
    db_ops.save_data(df, table_name=table_name)

if __name__ =='__main__':
    main()
