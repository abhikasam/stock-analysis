from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

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

@router.post("/",response_model=SymbolResponse)
def create_symbol(symbol:SymbolCreate,db:Session = Depends(get_db)):
    db_symbol = Symbol(**symbol.model_dump())
    db.add(db_symbol)
    db.commit()
    db.refresh(db_symbol)
    return db_symbol


@router.post("/bulk", response_model=List[SymbolResponse])
def bulk_insert(symbols: List[SymbolCreate], db: Session = Depends(get_db)):
    all_db_symbols = db.query(Symbol).all()
    db_symbols:List[Symbol] = []
    for symbol in symbols:
        if not all_db_symbols.__contains__(symbol.name) :
            db_symbol = Symbol(**symbol.model_dump())
            db.add(db_symbol)
            db.commit()
            db.refresh(db_symbol)
            db_symbols.append(db_symbol)
    return db_symbols

@router.delete("/bulk")
def bulk_delete(db:Session = Depends(get_db)):
    db.execute(text(f"delete from symbol"))
    db.commit()
    return []