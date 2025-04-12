from sqlalchemy import Column, Integer, String

from database import DataBase


class User(DataBase):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    name = Column(String,index=False)
    email=Column(String,unique=True,index=False)