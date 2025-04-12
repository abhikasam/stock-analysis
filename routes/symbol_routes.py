from http import HTTPStatus
from typing import List

import requests
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from core.config import Configuration
from models.database import SessionLocal
from models.symbol import Symbol
from schemas.symbol import SymbolResponse, SymbolCreate

router = APIRouter(
    prefix="/symbols",
    tags=["Symbol"]
)

#dependency to get DB session
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/",response_model=List[SymbolResponse])
def read_symbols(db:Session=Depends(get_db)):
    symbols = db.query(Symbol).all()
    return symbols

@router.get("/{symbol}/overview")
def read_overview(symbol:str):
    response = requests.get(f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}"
                            f"&apikey={Configuration.ALPHAVANTAGE_APIKEY}")
    return response.json()

@router.post("/",response_model=SymbolResponse)
def create_symbol(symbol:SymbolCreate,db:Session = Depends(get_db)):
    db_symbol = Symbol(**symbol.model_dump())
    db.add(db_symbol)
    db.commit()
    db.refresh(db_symbol)
    return db_symbol

@router.get("/{symbol}/time_series_daily")
def read_time_series_daily(symbol:str):
    response = requests.get(
            f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&"
            f"symbol={symbol}&apikey={Configuration.ALPHAVANTAGE_APIKEY}")
    return response.json()
