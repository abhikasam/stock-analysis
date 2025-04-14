from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models.database import Entity
from models.stock import portfolio_stock


class Portfolio(Entity):
    __tablename__="portfolio"
    id=Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("user.id"),index=True)
    stock_id = Column(Integer,ForeignKey("stock.id"))
    user = relationship("User",back_populates="portfolios")
    stocks = relationship("Stock",secondary=portfolio_stock,back_populates="portfolios")