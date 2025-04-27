from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from models.database import Entity

class User(Entity):
    __tablename__= "user"
    id=Column(Integer,primary_key=True,index=True)
    name = Column(String,index=False)
    email=Column(String,unique=True,index=False)
    hashed_password = Column(String)
    is_active = Column(Boolean)

    watch_lists = relationship("WatchList",back_populates="user")
    portfolios = relationship("Portfolio",back_populates="user")
