import sqlite3
import pandas as pd 

# make sure you are in src lvl to run the colde 

class HistoryPriceDataHandler():
    def __init__(self) -> None:
        self.db_name = 'td_stock_histroy.db'
        self.conn = sqlite3.connect(self.db_name) 

        self._schema = dict(open=float, high=float, 
            low=float, close=float, volume=int, datetime=int )

    def save_data(self, df, table_name):
        """save data to sql3 db 

        Args:
            df (pd.DataFrame): the table from td-ameritrate price history
            table_name (str): the table name 
        """
        df.to_sql(table_name, self.conn, if_exists='append', index=False) 
        self._clean_df(table_name=table_name)

    def _clean_df(self, table_name, key_col='datetime'):

        sql = f"""DELETE from {table_name} where rowid not in
            (SELECT min(rowid) from {table_name}
                group by {key_col});"""
        cur= self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()

    
    def get_hist_table_name(self, symbol, frequency_type, frequency):
        """to have a centralized naming rules for price-hist-table

        Args:
            symbol (str): stock name
            frequency_type (str): the frequency type from TD api
            frequency (int): the allowed frequency according to TD api

        Returns:
            _type_: _description_
        """
        return f"{symbol}_{frequency_type}_{frequency}"

    def read_hist_table(self, symbol, frequency_type, frequency, start_dt=None, end_dt=None):
        """_summary_

        Args:
            symbol (str): stock name
            frequency_type (str): the frequency type from TD api
            frequency (int): the allowed frequency according to TD api
            
            start_dt (str): start date in format '%Y-%M-%d'
            end_dt (str):  end date in format '%Y-%M-%d'

        Raises:
            ValueError: if table is not in BD

        Returns:
            pd.DataFrame : the data-frame that is ready for backtrader
        """
        table_name = self.get_hist_table_name(symbol, frequency_type, frequency)

        # select the data 
        df = pd.read_sql(f"SELECT * from {table_name}", self.conn)

        # data-type checks
        for k, v in self._schema.items():
            df[k] = df[k].astype(v)
        
        # convert from ms
        df.datetime = pd.to_datetime(df.datetime, unit='ms')
        if start_dt:
            start_dt = pd.to_datetime(start_dt)
            df = df[df.datetime >= start_dt]
        if end_dt:
            end_dt = pd.to_datetime(end_dt)
            df = df[df.datetime <= end_dt]

        df = df.set_index('datetime')


        return df 