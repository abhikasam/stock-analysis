from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from models.database import Entity


class Portfolio(Entity):
    __tablename__="portfolio"
    id=Column(Integer,primary_key=True,index=True)
    name = Column(String)
    user_id = Column(Integer,ForeignKey("user.id"),index=True)
    user = relationship("User",back_populates="portfolios")
    stocks = relationship("PortfolioStock",back_populates="portfolio")