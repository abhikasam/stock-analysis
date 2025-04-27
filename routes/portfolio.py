import json
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.PortfolioStock import PortfolioStock
from models.database import get_db
from models.portfolio import Portfolio
from models.stock import Stock
from models.user import User
from schemas.portfolio import PortfolioCreate, PortfolioResponse

router = APIRouter(
    prefix="/portfolios",
    tags=["Portfolio"]
)

db_dependency = Depends(get_db)

@router.get("/",response_model=List[PortfolioResponse])
def read_all_portfolios(db:Session = db_dependency):
    db_portfolios = db.query(Portfolio).all()
    portfolios=[]
    for db_portfolio in db_portfolios:
        portfolio = PortfolioResponse(
            name=db_portfolio.name,
            id=db_portfolio.id,
            user_id=db_portfolio.user_id
        )
        portfolios.append(portfolio)
    return portfolios


@router.get("/{portfolio_id}/stocks")
def read_portfolio(portfolio_id:int,db:Session = db_dependency):
    portfolio = db.query(Portfolio).filter_by(id=portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=400,detail="Portfolio not exists")
    if len(portfolio.stocks)==0:
        raise HTTPException(status_code=200,detail="No stock present in portfolio")
    return portfolio.stocks


@router.post("/",response_model=PortfolioResponse)
def insert_portfolio(portfolio_create:PortfolioCreate,db:Session = db_dependency):
    user_exists = db.query(User).filter_by(id=portfolio_create.user_id).first()
    if not user_exists:
        raise  HTTPException(status_code=400,detail="User not exists")
    record_exists = db.query(Portfolio).filter_by(name=portfolio_create.name,
                                                  user_id=portfolio_create.user_id).first()
    if record_exists:
        raise HTTPException(status_code=409,detail="Portfolio with this name already exists")
    db_portfolio = Portfolio(**portfolio_create.model_dump())
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio

@router.post("/import")
def import_data(db:Session = db_dependency):
    db_portfolios = []
    with open('db/portfolio.json') as file:
        portfolios = json.load(file)

        for portfolio in portfolios:
            db_portfolio = Portfolio(
                id=portfolio["id"],
                name=portfolio["name"],
                user_id=portfolio["user_id"]
            )
            db.add(db_portfolio)
            db.commit()
            db.refresh(db_portfolio)

            for stock in portfolio["stocks"]:
                stock_entry = db.query(Stock).filter_by(id = stock["id"]).first()
                if stock_entry:
                    db_portfolio_stock = PortfolioStock(
                        portfolio_id=db_portfolio.id,
                        stock_id=stock_entry.id
                    )
                    db.add(db_portfolio_stock)
            db.commit()
            db_portfolios.append(db_portfolio)

    return db_portfolios