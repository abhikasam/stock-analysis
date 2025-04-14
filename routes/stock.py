import json
import os.path
from http import HTTPStatus
from typing import List

import requests
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from core.config import Configuration
from models.database import SessionLocal, get_db
from models.stock import Stock
from schemas.stock import StockResponse, StockCreate

router = APIRouter(
    prefix="/stocks",
    tags=["Stock"]
)

@router.get("/", response_model=List[StockResponse])
def read_symbols(db:Session=Depends(get_db)):
    symbols = db.query(Stock).all()
    return symbols

@router.get("/{stock}/overview")
def read_overview(stock:str):
    response = requests.get(f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={stock}"
                            f"&apikey={Configuration.ALPHAVANTAGE_APIKEY}")
    return response.json()

@router.post("/", response_model=StockResponse)
def create_symbol(stock:StockCreate, db:Session = Depends(get_db)):
    db_symbol = Stock(**stock.model_dump())
    db.add(db_symbol)
    db.commit()
    db.refresh(db_symbol)
    return db_symbol

@router.get("/{stock}/time_series_daily")
def read_time_series_daily(stock:str):
    response = requests.get(
            f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&"
            f"symbol={stock}&apikey={Configuration.ALPHAVANTAGE_APIKEY}")
    return response.json()


@router.post("/bulk",response_model=List[StockResponse])
def insert_bulk(stocks_create:List[StockCreate],db:Session = Depends(get_db)):
    db_stocks = []
    if len(stocks_create) == 0:
        with open('db/stocks.json') as file:
            stocks = json.load(file)
            for stock in stocks:
                db_stock = Stock(**stock)
                db.add(db_stock)
                db.commit()
                db.refresh(db_stock)
                db_stocks.append(db_stock)
        pass
    else :
        all_symbols = db.query(Stock).with_entities(Stock.symbol).all()
        for stock in stocks_create:
            if stock.symbol not in all_symbols:
                db_stock = Stock(**stock.model_dump())
                db.add(db_stock)
                db.commit()
                db.refresh(db_stock)
                db_stocks.append(db_stock)
    return db_stocks
