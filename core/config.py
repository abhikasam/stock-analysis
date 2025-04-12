import os

from dotenv import load_dotenv


class Configuration:
    load_dotenv()
    ALPHAVANTAGE_APIKEY = os.getenv("API_KEY")
    SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
