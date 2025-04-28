from datetime import timedelta, datetime, timezone

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import  OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from core.config import Configuration
from models.database import get_db
from models.user import User
from jose import jwt

from schemas.token import Token

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

db_dependency = Depends(get_db)
bcrypt_context = CryptContext(schemes='bcrypt')

def authenticate_user(email:str,password:str,db:Session):
    user = db.query(User).filter_by(email=email).first()
    if not User:
        return False
    if not bcrypt_context.verify(password,user.hashed_password):
        return False
    return user

def create_access_token(username:str,user_id:int,expires_delta:timedelta):
    encode = { 'sub': username,'id': user_id }
    expires =  datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})
    token = jwt.encode(encode,Configuration.JWT_SECRET_KEY,algorithm=Configuration.JWT_ALGORITHM)
    return Token(access_token=token,token_type='bearer')


@router.post('/login',response_model=Token)
def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=db_dependency):
    print(form_data.username,form_data.password)
    user = authenticate_user(form_data.username,form_data.password,db)
    if not user:
        return 'Failed authentication.'
    token = create_access_token(user.email,user.id,timedelta(minutes=20))
    return token

