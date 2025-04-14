from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from models.database import Entity

portfolio_stock = Table(
    'portfolio_stock',Entity.metadata,
    Column('portfolio_id',Integer,ForeignKey("portfolio.id")),
    Column('stock_id',Integer,ForeignKey('stock.id'))
)

class Stock(Entity):
    __tablename__= "stock"
    id = Column(Integer,primary_key=True,index=True)
    symbol = Column(String,index=True)
    description = Column(String,index=False)

    portfolios = relationship("Portfolio",secondary=portfolio_stock,back_populates="stocks")