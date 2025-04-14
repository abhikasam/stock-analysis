from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.database import get_db
from models.portfolio import Portfolio
from models.user import User

router = APIRouter(
    prefix="/portfolios",
    tags=["Portfolio"]
)

db_dependency = Depends(get_db)

