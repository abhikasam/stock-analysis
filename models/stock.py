from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from models.database import Entity

class Stock(Entity):
    __tablename__= "stock"
    id = Column(Integer,primary_key=True,index=True)
    symbol = Column(String,index=True)
    description = Column(String,index=False)

    portfolios = relationship("PortfolioStock",back_populates="stock")