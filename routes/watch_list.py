from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.annotation import Annotated

from models.database import SessionLocal, get_db
from models.user import User
from models.watch_list import WatchList
from schemas.watch_list import WatchListCreate

router=APIRouter(
    prefix="/watchlists",
    tags=["Watchlist"]
)

@router.get("/all")
def read_all(db:Session = Depends(get_db)):
    watch_lists = db.query(WatchList).all()
    return watch_lists

@router.post("/")
def add_watch_list(watch_list:WatchListCreate,db:Session = Depends(get_db)):
    db_watch_lists = db.query(WatchList).all()
    existing = db.query(WatchList).filter(WatchList.name==watch_list.name and WatchList.user_id==watch_list.user_id).first()
    if existing:
        return HTTPException(status_code=409,detail="User already has this name for a watchlist.")
    user = db.query(User).filter(User.id==watch_list.user_id).first()
    if not user:
        return HTTPException(status_code=400,detail="User not found")
    db_watch_list = WatchList(**watch_list.model_dump())
    db.add(db_watch_list)
    db.commit()
    db.refresh(db_watch_list)
    return db_watch_list


