from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models.database import Entity


class WatchList(Entity):
    __tablename__="watchlist"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    user_id = Column(Integer,ForeignKey("user.id"),index=True)

    user = relationship("User",back_populates="watch_lists")
