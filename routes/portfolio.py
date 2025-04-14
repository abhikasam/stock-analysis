from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

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

@router.get("/{portfolio_id}")
def read_portfolio(portfolio_id:int,db:Session = db_dependency):
    portfolio = db.query(Portfolio).filter_by(id=portfolio_id).first()
    if not portfolio:
        raise HTTPException(status_code=400,detail="Portfolio not exists")
    if len(portfolio.stocks)==0:
        raise HTTPException(status_code=200,detail="No stock present in portfolio")
    return portfolio.stocks


@router.post("/",response_model=PortfolioResponse)
def insert_portfolio(portfolio_create:PortfolioCreate,db:Session = db_dependency):
    stock_exists = db.query(Stock).filter_by(id=portfolio_create.stock_id).first()
    if not stock_exists:
        raise HTTPException(status_code=400,detail="Stock not exists")
    user_exists = db.query(User).filter_by(id=portfolio_create.user_id).first()
    if not user_exists:
        raise  HTTPException(status_code=400,detail="User not exists")
    record_exists = db.query(Portfolio).filter_by(user_id=portfolio_create.user_id
                                                  ,stock_id= portfolio_create.stock_id).first()
    if record_exists:
        raise HTTPException(status_code=409,detail="Stock is already present in user's portfolio")
    db_portfolio = Portfolio(**portfolio_create.model_dump())
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio
