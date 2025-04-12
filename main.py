# This is a sample Python script.
import json
import traceback
# Press Ctrl+F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv
import re

from core.config import Configuration
from models.database import DataBase, engine
from routes.user_routes import router as user_router
from routes.symbol_routes import router as symbol_router

# Create tables
DataBase.metadata.create_all(bind=engine)


app=FastAPI()

app.include_router(user_router)
app.include_router(symbol_router)


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print("Hello")

