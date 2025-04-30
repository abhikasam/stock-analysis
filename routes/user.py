import json
import os.path
from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette import status

from models.database import get_db
from routes.auth import get_current_user
from schemas.user import UserCreate, UserResponse, UserQuery
from models.user import User
from passlib.context import CryptContext

router = APIRouter(
    prefix="/users",
    tags=["User"]
)

db_dependency = Depends(get_db)
user_dependency = Depends(get_current_user)
bcrypt_context = CryptContext(schemes=['bcrypt'])


@router.get("/",response_model=List[UserQuery])
def read_users(db:Session = db_dependency,current_user=user_dependency):
    users = db.query(User).all()
    user_results:List[UserQuery] = [
        UserQuery(
            id = user.id,
            email= user.email,
            name= user.name,
            is_active= user.is_active
        )
        for user in users
    ]
    return user_results

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = db_dependency):
    user = db.query(User).filter_by(id = user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = db_dependency):
    existing = db.query(User).filter_by(email=user.email).first()
    if existing:
        raise HTTPException(status_code=400,detail="Email already registered")
    db_user = User(
        email = user.email,
        name = user.name,
        hashed_password = bcrypt_context.hash(user.password),
        is_active = True
    )
    db.add(db_user)
    db.commit()


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
                db_user = User(
                    email=user.email,
                    hashed_password=bcrypt_context.hash(user.password),
                    name=user.name,
                    is_active=True
                )
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
        user_jsons:List[UserCreate] = [ UserCreate(**u) for u in users]
        for user in user_jsons:
            db_user = User(
                email = user.email,
                hashed_password = bcrypt_context.hash(user.password),
                name = user.name,
                is_active = True
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            db_users.append(db_user)
    return db_users
