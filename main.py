# This is a sample Python script.
import json
import traceback
# Press Ctrl+F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv
import re

from core.config import Configuration
from models.database import DataBase, engine
from routes.user_routes import router as user_router
from routes.symbol_routes import router as symbol_router

# Create tables
DataBase.metadata.create_all(bind=engine)


app=FastAPI()

app.include_router(user_router)
app.include_router(symbol_router)

@app.get("/")
def read_data():
    return { "message" : "Hello World" }

@app.get("/stock/{symbol}")
def read_api(symbol:str):
    try:
        response = requests.get(
            f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={Configuration.ALPHAVANTAGE_APIKEY}")
        symbol_daily_analysis = json.loads(response.text)
        symbol_daily_analysis_items = {}
        for key, value in symbol_daily_analysis["Time Series (Daily)"].items():
            print(key, value)
            symbol_daily_analysis_item = {}
            for ikey, ivalue in value.items():
                symbol_daily_analysis_item[re.search(r'\d+\.\s*(\w+)', ikey).group(1)] = ivalue
            symbol_daily_analysis_items[key] = symbol_daily_analysis_item
        return symbol_daily_analysis_items
    except Exception as e:
        print(traceback.format_exc())
        return str(e)

# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print("Hello")

