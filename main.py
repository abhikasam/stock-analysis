# This is a sample Python script.
import json
import traceback
from contextlib import asynccontextmanager

# Press Ctrl+F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv
import re

from core.config import Configuration
from models.database import Entity, engine
from routes import user, stock, watch_list, portfolio

# Create tables
Entity.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(user.router)
app.include_router(stock.router)
app.include_router(watch_list.router)
app.include_router(portfolio.router)




# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print("Hello")

