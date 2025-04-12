from sqlalchemy import Column, Integer, String

from models.database import DataBase


class User(DataBase):
    __tablename__= "user"
    id=Column(Integer,primary_key=True,index=True)
    name = Column(String,index=False)
    email=Column(String,unique=True,index=False)