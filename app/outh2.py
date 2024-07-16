from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt, pytz
from typing import Union, Annotated
from . import schema
from datetime import timedelta, timezone, datetime
from fastapi import Depends, HTTPException, status
from .repository.user import UserRepository
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError
SECRET_KEY = "217ef8ad7e90a57b940c97a402258499cdd7b483d39637b7d48d0468a56e0f8c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict,expires_delta:Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(pytz.timezone('Africa/Tripoli')) + expires_delta
    else:
        expire = datetime.now(pytz.timezone('Africa/Tripoli')) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = schema.TokenData(username=username,site_id=payload.get("site_id"),user_type=payload.get("user_type"))
    except InvalidTokenError:
        raise credentials_exception
    return token_data

async def refreshToken(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM],options={"verify_signature": False})
    token_data = {"username":payload.get("username"),"site_id":payload.get("site_id"), "user_type":payload.get("user_type")}
    return create_access_token(token_data)