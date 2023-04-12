from borsdata_api import BorsdataAPI
import mysql.connector as msql
import pandas as pd
import datetime as dt
import time
import constants


# this function needs to be runned once to create database and tables.
def create_database(host: str, user: str, password: str, db_name: str):
    print(f"Creating database: {db_name}")
    # create connection to MYSQL (no database selected)
    connection = msql.connect(
        host=host, user=user, password=password, database="")
    cursor = connection.cursor()
    # create schema (database)
    cursor.execute(f"CREATE SCHEMA {db_name}")
    # reconnect to newly created schema (database)
    connection = msql.connect(
        host=host, user=user, password=password, database=db_name)
    cursor = connection.cursor()
    # create new tables under schema (database)
    cursor.execute(constants.STOCKS)
    cursor.execute(constants.STOCK_PRICES)
    cursor.execute(constants.REPORTS_YEAR)
    cursor.execute(constants.REPORTS_R12)
    cursor.execute(constants.REPORTS_QUARTER)
    print("Database and tables created!")


class DatabaseUpdater:
    def __init__(self):
        self._borsdata_api = BorsdataAPI(constants.API_KEY)
        self._db_connection = msql.connect(
            host=constants.DB_HOST, user=constants.DB_USER, password=constants.DB_PW, database=constants.DB_NAME)
        self._cursor = self._db_connection.cursor()
        self._instruments = self._borsdata_api.get_instruments()
        self._instruments['country'] = self._instruments['countryId'].map(
            {1: "Sverige", 2: "Norge", 3: "Finland", 4: "Danmark"})
        self._instruments['instrument'] = self._instruments['instrument'].map({0:	'Stocks',
                                                                               1:	'Pref',
                                                                               2:	'NordicIndex',
                                                                               3:	'Stocks2',
                                                                               4:	'Sector',
                                                                               5:	'Industry',
                                                                               6:	'Currency',
                                                                               7:	'Commodity',
                                                                               8:	'SPAC',
                                                                               9:	'ADR',
                                                                               10:	'Unit',
                                                                               11:	'GlobalIndex',
                                                                               12:	'Cryptocurrencies',
                                                                               13:	'NordicOtherIndex'})

        self._markets = self._borsdata_api.get_markets()
        self._countries = self._borsdata_api.get_countries()
        self._sectors = self._borsdata_api.get_sectors()
        self._branches = self._borsdata_api.get_branches()
        self._updated_instruments = self._borsdata_api.get_instruments_updated()

    def _create_stock_id_list(self, instruments: pd.DataFrame = None, length: int = 50):
        if instruments is None:
            instruments = self._instruments
        list_of_stock_ids = []
        temp = []
        ctr = 0
        for ins_id, _instrument in instruments.iterrows():
            temp.append(ins_id)
            ctr += 1
            if ctr == length:
                list_of_stock_ids.append(temp.copy())
                temp.clear()
                ctr = 0
        return list_of_stock_ids

    def update_stock_data(self):
        print("DatabaseUpdater >> Updating Stock Data")
        for ins_id, instrument in self._instruments.iterrows():
            name = instrument['name']
            ticker = instrument['ticker']
            ticker_yahoo = instrument['yahoo']
            isin = instrument['isin']
            listing_date = pd.to_datetime(instrument['listingDate'])
            listing_date = listing_date.date()
            instrument_type = instrument['instrument']
            market = self._markets.loc[self._markets.index
                                       == instrument['marketId']]['name'].values[0]
            country = self._countries.loc[self._countries.index
                                          == instrument['countryId']]['name'].values[0]
            sector = 'N/A'
            branch = 'N/A'
            if market.lower() == 'index':
                sector = 'N/A'
                branch = 'N/A'
            else:
                sector = self._sectors.loc[self._sectors.index
                                           == instrument['sectorId']]['name'].values[0]
                branch = self._branches.loc[self._branches.index
                                            == instrument['branchId']]['name'].values[0]
            sql = f"REPLACE INTO stocks(stock_id, name, ticker, ticker_yahoo, market, sector, branch, country, "\
                  f"type, isin, listing_date) VALUES ({ins_id}, '{name}', '{ticker}', '{ticker_yahoo}', "\
                  f"'{market}', '{sector}', '{branch}', '{country}', '{instrument_type}', '{isin}', '{listing_date}')"
            try:
                self._cursor.execute(sql)
            except Exception as e:
                print(e)
        self._db_connection.commit()

    def update_stock_prices_list(self, from_date: dt.datetime = None, to_date: dt.datetime = None):
        print("DatabaseUpdater >> Updating Stock Prices Data with Lists")
        sql_many = "REPLACE INTO stock_prices(stock_id, date, high, low, close, open, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        start = time.time()
        checkpoint = start
        list_of_stock_ids = self._create_stock_id_list(length=50)
        for stock_id_list in list_of_stock_ids:
            df = self._borsdata_api.get_instrument_stock_prices_list(
                stock_id_list, from_date=from_date, to_date=to_date)
            print(f"Trying to insert all, length of df: {len(df)}")
            # NaN values filled with 0
            df = df.fillna(0)
            self._cursor.executemany(sql_many, df[[
                                     'stock_id', 'date', 'high', 'low', 'close', 'open', 'volume']].values.tolist())
            self._db_connection.commit()
            end = time.time()
            print(
                f"Inserted: {stock_id_list} time: {end - checkpoint:.1f} seconds")
            checkpoint = end
        print(f"All data inserted, total time {time.time()-start:.1f}")

    def update_report_data_list(self, just_today: bool = False):
        print("DatabaseUpdater >> Updating Report Data")
        if just_today:
            instruments_metadata = self._updated_instruments
            instrument_list = self._instruments[self._instruments.index.isin(
                instruments_metadata.index)]
            instrument_list = self._create_stock_id_list(instrument_list)
        else:
            instrument_list = self._create_stock_id_list()
        for ids in instrument_list:
            reports_quarter, reports_year, reports_r12 = self._borsdata_api.get_instrument_report_list(
                ids)
            print(
                f"DatabaseUpdater >> Inserting Report data for stock_ids: {ids}")
            for report_type, df in {'reports_quarter': reports_quarter, 'reports_year': reports_year, 'reports_r12': reports_r12}.items():
                df['report_date'].replace(
                    0, dt.datetime(1970, 1, 1), inplace=True)
                # NaN values filled with 0
                df = df.fillna(0)
                sql = f"REPLACE INTO {report_type} (year, stock_id, broken_fiscal_year," \
                      f"cash_and_equivalents, cash_flow_for_the_year, cash_flow_from_financing_activities," \
                      f"cash_flow_from_investing_activities, cash_flow_from_operating_activities, current_assets," \
                      f"current_liabilities, dividend, earnings_per_share, financial_assets, free_cash_flow, " \
                      f"gross_income, intangible_assets, net_debt, non_current_assets, non_current_liabilities, " \
                      f"number_of_shares, operating_income, period, profit_before_tax, profit_to_equity_holders, " \
                      f"report_end_date, report_start_date, revenues, stock_price_average, stock_price_high, " \
                      f"stock_price_low, tangible_assets, total_assets, total_equity, " \
                      f"total_liabilities_and_equity, currency, currency_ratio, net_sales, report_date) VALUES " \
                      f"(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
                      f" %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                try:
                    cols = ["year", "stock_id", "broken_fiscal_year", "cash_and_equivalents", "cash_flow_for_the_year",
                            "cash_flow_from_financing_activities", "cash_flow_from_investing_activities",
                            "cash_flow_from_operating_activities", "current_assets", "current_liabilities",
                            "dividend", "earnings_per_share", "financial_assets", "free_cash_flow",
                            "gross_income", "intangible_assets", "net_debt", "non_current_assets",
                            "non_current_liabilities",
                            "number_of_shares", "operating_income", "period", "profit_before_tax",
                            "profit_to_equity_holders",
                            "report_end_date", "report_start_date", "revenues", "stock_price_average",
                            "stock_price_high",
                            "stock_price_low", "tangible_assets", "total_assets", "total_equity",
                            "total_liabilities_and_equity", "currency", "currency_ratio", "net_sales", "report_date"]
                    self._cursor.executemany(sql, df[cols].values.tolist())
                    self._db_connection.commit()
                except Exception as e:
                    print(e)
                    continue


if __name__ == "__main__":
    create_database(constants.DB_HOST, constants.DB_USER,
                    constants.DB_PW, constants.DB_NAME)
    db_updater = DatabaseUpdater()
    db_updater.update_stock_data()
    db_updater.update_stock_prices_list(from_date=dt.datetime(2020, 1, 1))
    db_updater.update_report_data_list()
