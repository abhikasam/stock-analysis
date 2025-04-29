from datetime import timedelta, datetime, timezone

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from starlette import status

from core.config import Configuration
from models.database import get_db
from models.user import User
from jose import jwt, JWTError

from schemas.token import Token

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

db_dependency = Depends(get_db)
bcrypt_context = CryptContext(schemes=['bcrypt'])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')

def authenticate_user(email:str,password:str,db:Session):
    user = db.query(User).filter_by(email=email).first()
    if not user:
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

async def get_current_user(token:str=Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token,Configuration.JWT_SECRET_KEY,algorithms=Configuration.JWT_ALGORITHM)
        username : str = payload.get('sub')
        user_id : int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='Could not validate user.')


@router.post('/login',response_model=Token)
def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=db_dependency):
    user = authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate user.')
    token = create_access_token(user.email,user.id,timedelta(minutes=20))
    return token

