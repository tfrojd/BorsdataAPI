"""
User constants
"""
API_KEY = 'xxx'
EXPORT_PATH = 'file_exports/'
DB_USER = "root"
DB_PW = ""
DB_NAME = "borsdata"
DB_HOST = "localhost"


STOCKS = """CREATE TABLE `stocks` (
  `stock_id` int unsigned NOT NULL,
  `name` varchar(60) DEFAULT NULL,
  `ticker` varchar(20) DEFAULT NULL,
  `ticker_yahoo` varchar(20) DEFAULT NULL,
  `market` varchar(20) DEFAULT NULL,
  `sector` varchar(50) DEFAULT NULL,
  `branch` varchar(60) DEFAULT NULL,
  `country` varchar(45) DEFAULT NULL,
  `type` varchar(20) DEFAULT NULL,
  `isin` varchar(45) DEFAULT NULL,
  `listing_date` datetime DEFAULT NULL,
  PRIMARY KEY (`stock_id`),
  KEY `stock_id` (`stock_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""

STOCK_PRICES = """CREATE TABLE `stock_prices` (
  `stock_id` int unsigned NOT NULL,
  `date` datetime NOT NULL,
  `high` float DEFAULT NULL,
  `low` float DEFAULT NULL,
  `close` float DEFAULT NULL,
  `open` float DEFAULT NULL,
  `volume` bigint DEFAULT NULL,
  PRIMARY KEY (`stock_id`,`date`),
  KEY `stock_id_stock_prices` (`stock_id`),
  CONSTRAINT `fk_stock_prices_id` FOREIGN KEY (`stock_id`) REFERENCES `stocks` (`stock_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""

REPORTS_YEAR = """CREATE TABLE `reports_year` (
  `year` int unsigned NOT NULL,
  `stock_id` int unsigned NOT NULL,
  `broken_fiscal_year` tinyint(1) DEFAULT NULL,
  `cash_and_equivalents` float DEFAULT NULL,
  `cash_flow_for_the_year` float DEFAULT NULL,
  `cash_flow_from_financing_activities` float DEFAULT NULL,
  `cash_flow_from_investing_activities` float DEFAULT NULL,
  `cash_flow_from_operating_activities` float DEFAULT NULL,
  `current_assets` float DEFAULT NULL,
  `current_liabilities` float DEFAULT NULL,
  `dividend` float DEFAULT NULL,
  `earnings_per_share` float DEFAULT NULL,
  `financial_assets` float DEFAULT NULL,
  `free_cash_flow` float DEFAULT NULL,
  `gross_income` float DEFAULT NULL,
  `intangible_assets` float DEFAULT NULL,
  `net_debt` float DEFAULT NULL,
  `non_current_assets` float DEFAULT NULL,
  `non_current_liabilities` float DEFAULT NULL,
  `number_of_shares` float DEFAULT NULL,
  `operating_income` float DEFAULT NULL,
  `period` float DEFAULT NULL,
  `profit_before_tax` float DEFAULT NULL,
  `profit_to_equity_holders` float DEFAULT NULL,
  `report_end_date` datetime DEFAULT NULL,
  `report_start_date` datetime DEFAULT NULL,
  `revenues` float DEFAULT NULL,
  `stock_price_average` float DEFAULT NULL,
  `stock_price_high` float DEFAULT NULL,
  `stock_price_low` float DEFAULT NULL,
  `tangible_assets` float DEFAULT NULL,
  `total_assets` float DEFAULT NULL,
  `total_equity` float DEFAULT NULL,
  `total_liabilities_and_equity` float DEFAULT NULL,
  `currency` varchar(45) DEFAULT NULL,
  `currency_ratio` float DEFAULT NULL,
  `net_sales` float DEFAULT NULL,
  `report_date` datetime DEFAULT NULL,
  PRIMARY KEY (`year`,`stock_id`),
  KEY `st` (`stock_id`),
  CONSTRAINT `fk_year` FOREIGN KEY (`stock_id`) REFERENCES `stocks` (`stock_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""

REPORTS_R12 = """CREATE TABLE `reports_r12` (
  `year` int NOT NULL,
  `stock_id` int unsigned NOT NULL,
  `broken_fiscal_year` tinyint(1) DEFAULT NULL,
  `cash_and_equivalents` float DEFAULT NULL,
  `cash_flow_for_the_year` float DEFAULT NULL,
  `cash_flow_from_financing_activities` float DEFAULT NULL,
  `cash_flow_from_investing_activities` float DEFAULT NULL,
  `cash_flow_from_operating_activities` float DEFAULT NULL,
  `current_assets` float DEFAULT NULL,
  `current_liabilities` float DEFAULT NULL,
  `dividend` float DEFAULT NULL,
  `earnings_per_share` float DEFAULT NULL,
  `financial_assets` float DEFAULT NULL,
  `free_cash_flow` float DEFAULT NULL,
  `gross_income` float DEFAULT NULL,
  `intangible_assets` float DEFAULT NULL,
  `net_debt` float DEFAULT NULL,
  `non_current_assets` float DEFAULT NULL,
  `non_current_liabilities` float DEFAULT NULL,
  `number_of_shares` float DEFAULT NULL,
  `operating_income` float DEFAULT NULL,
  `period` float NOT NULL,
  `profit_before_tax` float DEFAULT NULL,
  `profit_to_equity_holders` float DEFAULT NULL,
  `report_end_date` datetime DEFAULT NULL,
  `report_start_date` datetime DEFAULT NULL,
  `revenues` float DEFAULT NULL,
  `stock_price_average` float DEFAULT NULL,
  `stock_price_high` float DEFAULT NULL,
  `stock_price_low` float DEFAULT NULL,
  `tangible_assets` float DEFAULT NULL,
  `total_assets` float DEFAULT NULL,
  `total_equity` float DEFAULT NULL,
  `total_liabilities_and_equity` float DEFAULT NULL,
  `currency` varchar(45) DEFAULT NULL,
  `currency_ratio` float DEFAULT NULL,
  `net_sales` float DEFAULT NULL,
  `report_date` datetime DEFAULT NULL,
  PRIMARY KEY (`year`,`stock_id`,`period`),
  KEY `fk_stock_id_idx` (`stock_id`),
  CONSTRAINT `fk_stock_id2` FOREIGN KEY (`stock_id`) REFERENCES `stocks` (`stock_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""

REPORTS_QUARTER = """CREATE TABLE `reports_quarter` (
  `year` int NOT NULL,
  `stock_id` int unsigned NOT NULL,
  `broken_fiscal_year` tinyint(1) DEFAULT NULL,
  `cash_and_equivalents` float DEFAULT NULL,
  `cash_flow_for_the_year` float DEFAULT NULL,
  `cash_flow_from_financing_activities` float DEFAULT NULL,
  `cash_flow_from_investing_activities` float DEFAULT NULL,
  `cash_flow_from_operating_activities` float DEFAULT NULL,
  `current_assets` float DEFAULT NULL,
  `current_liabilities` float DEFAULT NULL,
  `dividend` float DEFAULT NULL,
  `earnings_per_share` float DEFAULT NULL,
  `financial_assets` float DEFAULT NULL,
  `free_cash_flow` float DEFAULT NULL,
  `gross_income` float DEFAULT NULL,
  `intangible_assets` float DEFAULT NULL,
  `net_debt` float DEFAULT NULL,
  `non_current_assets` float DEFAULT NULL,
  `non_current_liabilities` float DEFAULT NULL,
  `number_of_shares` float DEFAULT NULL,
  `operating_income` float DEFAULT NULL,
  `period` float NOT NULL,
  `profit_before_tax` float DEFAULT NULL,
  `profit_to_equity_holders` float DEFAULT NULL,
  `report_end_date` datetime DEFAULT NULL,
  `report_start_date` datetime DEFAULT NULL,
  `revenues` float DEFAULT NULL,
  `stock_price_average` float DEFAULT NULL,
  `stock_price_high` float DEFAULT NULL,
  `stock_price_low` float DEFAULT NULL,
  `tangible_assets` float DEFAULT NULL,
  `total_assets` float DEFAULT NULL,
  `total_equity` float DEFAULT NULL,
  `total_liabilities_and_equity` float DEFAULT NULL,
  `currency` varchar(45) DEFAULT NULL,
  `currency_ratio` float DEFAULT NULL,
  `net_sales` float DEFAULT NULL,
  `report_date` datetime DEFAULT NULL,
  PRIMARY KEY (`year`,`stock_id`,`period`),
  KEY `stock_id` (`stock_id`),
  CONSTRAINT `fk_stock_id` FOREIGN KEY (`stock_id`) REFERENCES `stocks` (`stock_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""