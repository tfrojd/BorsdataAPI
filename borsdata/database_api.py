import mysql.connector as mdb
import pandas as pd
import numpy as np
import constants
from typing import List


class DataBaseAPI:
    def __init__(self):
        self._connection = mdb.connect(
            host=constants.DB_HOST, user=constants.DB_USER, password=constants.DB_PW, database=constants.DB_NAME)
        self._cursor = self._connection.cursor()

    def get_all_stock_data(self, where: str = "") -> pd.DataFrame:
        sql_query = f"SELECT * FROM stocks {where}"
        self._cursor.execute(sql_query)
        records = list(self._cursor.fetchall())
        df = pd.DataFrame(records, columns=['stock_id', 'name', 'ticker', 'ticker_yahoo', 'market', 'sector', 'branch', 'country',
                                            'type',  'isin', 'listing_date'])
        return df

    def get_all_stock_prices(self, where: str = "") -> pd.DataFrame:
        sql_query = f"SELECT * FROM stock_prices {where}"
        self._cursor.execute(sql_query)
        records = list(self._cursor.fetchall())
        df = pd.DataFrame(records, columns=[
                          'stock_id', 'date', 'high', 'low', 'close', 'open', 'volume'])
        df['date'] = pd.to_datetime(df['date'])
        return df

    def get_all_report_data(self, type: str, where: str = "") -> pd.DataFrame:
        if type not in ["year", "r12", "quarter"]:
            print("Unsupported table, supported tables are 'year', 'r12', 'quarter")
        sql_query = f"SELECT * FROM reports_{type} {where}"
        self._cursor.execute(sql_query)
        records = list(self._cursor.fetchall())
        cols = ['year', 'stock_id', 'broken_fiscal_year', 'cash_and_equivalents', 'cash_flow_for_the_year',
                'cash_flow_from_financing_activities', 'cash_flow_from_investing_activities',
                'cash_flow_from_operating_activities', 'current_assets', 'current_liabilities',
                'dividend', 'earnings_per_share', 'financial_assets', 'free_cash_flow', 'gross_income',
                'intangible_assets', 'net_debt', 'non_current_assets', 'non_current_liabilities', 'number_of_shares',
                'operating_income', 'period', 'profit_before_tax', 'profit_to_equity_holders', 'report_end_date',
                'report_start_date', 'revenues', 'stock_price_average', 'stock_price_high', 'stock_price_low',
                'tangible_assets', 'total_assets', 'total_equity', 'total_liabilities_and_equity', 'currency', 'currency_ratio', 'net_sales', 'report_date']
        df = pd.DataFrame(records, columns=cols)
        df.replace(0, np.nan, inplace=True)
        df = df.sort_values(by=['report_end_date'], ascending=[True])
        df.reset_index(inplace=True, drop=True)
        return df

    def get_with_query_string(self, sql_query: str, cols: List[str]) -> pd.DataFrame:
        self._cursor.execute(sql_query)
        records = list(self._cursor.fetchall())
        df = pd.DataFrame(records, columns=cols)
        return df


if __name__ == "__main__":
    db_api = DataBaseAPI()
    print(db_api.get_all_stock_data().tail())
    print("############")
    print(db_api.get_all_stock_data("WHERE stocks.market = 'First North'").tail())
    print("############")
    print(db_api.get_all_stock_prices(
        "WHERE stock_prices.date > '2023-01-01'").tail())
    print("############")
    print(db_api.get_all_report_data(
        "quarter", "WHERE reports_quarter.stock_id = 111"))
    print("############")
    query = """SELECT stock_prices.stock_id, stock_prices.date, stocks.name, stock_prices.high,
            stock_prices.low, stock_prices.close, stock_prices.open, stock_prices.volume FROM stock_prices
            INNER JOIN stocks ON stock_prices.stock_id = stocks.stock_id AND stocks.type = 'Stocks' WHERE stock_prices.date > '2023-01-01'"""
    columns = ["stock_id", "date", "name",
               "high", "low", "close", "open", "volume"]
    print(db_api.get_with_query_string(query, columns).tail())
