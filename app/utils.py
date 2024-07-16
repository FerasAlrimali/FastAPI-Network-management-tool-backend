from datetime import datetime, timedelta, timezone
from typing import Annotated, Union
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

SECRET_KEY = "217ef8ad7e90a57b940c97a402258499cdd7b483d39637b7d48d0468a56e0f8c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ip_regex = "^(?:(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plainPassword: str,hashedPassword: str):
    return pwd_context.verify(plainPassword,hashedPassword)