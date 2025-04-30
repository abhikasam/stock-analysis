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
from models.user import User
from routes.auth import get_current_user
from schemas.stock import StockResponse, StockCreate

router = APIRouter(
    prefix="/stocks",
    tags=["Stock"]
)

db_dependency : Session = Depends(get_db)
user_dependency = Depends(get_current_user)

@router.get("/all", response_model=List[StockResponse])
def read_stocks(db=db_dependency):
    stocks = db.query(Stock).all()
    return stocks

@router.get("/")
def read_stocks(db=db_dependency,user = user_dependency):
    print(user.get('id'))
    portfolios = db.query(User).filter_by(id=user.get('id')).first().portfolios
    all_stocks = [ stock for portfolio in portfolios for stock in portfolio.stocks]
    return all_stocks

@router.get("/{stock}/overview")
def read_overview(stock:str):
    print(Configuration.ALPHAVANTAGE_STOCK_OVERVIEW_URL.format(symbol=stock))
    response = requests.get(Configuration.ALPHAVANTAGE_STOCK_OVERVIEW_URL.format(symbol=stock))
    return response.json()

@router.post("/", response_model=StockResponse)
def create_symbol(stock:StockCreate, db:Session = Depends(get_db)):
    db_stock = Stock(**stock.model_dump())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

@router.get("/{stock}/time_series_daily")
def read_time_series_daily(stock:str):
    response = requests.get(Configuration.ALPHAVANTAGE_TIME_SERIES_DAILY_URL.format(symbol=stock))
    return response.json()


@router.post("/bulk",response_model=List[StockResponse])
def insert_bulk(stocks_create:List[StockCreate],db:Session = Depends(get_db)):
    db_stocks = []
    if len(stocks_create) != 0:
        all_symbols = db.query(Stock).with_entities(Stock.symbol).all()
        for stock in stocks_create:
            if stock.symbol not in all_symbols:
                db_stock = Stock(**stock.model_dump())
                db.add(db_stock)
                db.commit()
                db.refresh(db_stock)
                db_stocks.append(db_stock)
    return db_stocks

@router.post("/import",response_model=List[StockResponse])
def import_stocks(db:Session = db_dependency):
    db_stocks = []
    with open('db/stocks.json') as file:
        stocks = json.load(file)
        for stock in stocks:
            db_stock = Stock(**stock)
            db.add(db_stock)
            db.commit()
            db.refresh(db_stock)
            db_stocks.append(db_stock)
    return db_stocks
