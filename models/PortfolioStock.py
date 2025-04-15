from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models.database import Entity


class PortfolioStock(Entity):
    __tablename__ = 'portfolio_stock'

    portfolio_id = Column(Integer, ForeignKey("portfolio.id"), primary_key=True)
    stock_id = Column(Integer, ForeignKey("stock.id"), primary_key=True)
    portfolio = relationship("Portfolio", back_populates="stocks")
    stock = relationship("Stock", back_populates="portfolios")