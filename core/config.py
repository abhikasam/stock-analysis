import os

from dotenv import load_dotenv


class Configuration:
    load_dotenv()
    ALPHAVANTAGE_APIKEY = os.getenv("API_KEY")
    SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
    ALPHAVANTAGE_STOCK_OVERVIEW_URL = os.getenv("ALPHAVANTAGE_STOCK_OVERVIEW_URL")
    ALPHAVANTAGE_TIME_SERIES_DAILY_URL = os.getenv("ALPHAVANTAGE_TIME_SERIES_DAILY_URL")
