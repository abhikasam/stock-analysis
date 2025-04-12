from sqlalchemy import Column, Integer, String

from models.database import DataBase


class Symbol(DataBase):
    __tablename__= "symbol"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,index=True)
    description = Column(String,index=False)