import json
import os.path
from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from models.database import SessionLocal, engine, Entity, get_db
from models.watch_list import WatchList
from routes.portfolio import db_dependency
from schemas.user import UserCreate,UserResponse
from models.user import User

router = APIRouter(
    prefix="/users",
    tags=["User"]
)

db_dependency = Depends(get_db)

@router.get("/", response_model=List[UserResponse])
def read_users(db:Session = db_dependency):
    users = db.query(User).all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = db_dependency):
    user = db.query(User).filter_by(id = user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = db_dependency):
    existing = db.query(User).filter_by(email=user.email).first()
    if existing:
        raise HTTPException(status_code=400,detail="Email already registered")
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/{user_id}/watchlists")
def read_watchlists(user_id:int,db:Session=db_dependency):
    user = db.query(User).filter_by(id=user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user.watch_lists

@router.get("/{user_id}/portfolios")
def read_portfolios(user_id:int,db:Session=db_dependency):
    user = db.query(User).filter_by(id=user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user.portfolios

@router.post("/bulk")
def insert_user(users_create:List[UserCreate],db:Session= db_dependency):
    db_users = []
    if len(users_create) != 0:
        all_users = db.query(User).with_entities(User.email).all()
        for user in users_create:
            if user.email not in all_users:
                db_user = User(**user.model_dump())
                db.add(db_user)
                db.commit()
                db.refresh(db_user)
                db_users.append(db_user)
    return db_users

@router.post("/import")
def import_data(db:Session = db_dependency):
    db_users = []
    with open('db/users.json') as file:
        users = json.load(file)
        for user in users:
            db_user = User(**user)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            db_users.append(db_user)
    return db_users
