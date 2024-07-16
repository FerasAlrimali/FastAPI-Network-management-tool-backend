from fastapi import APIRouter, HTTPException, Depends,status,Header
from sqlalchemy.orm import Session
from ..repository.user import UserRepository
from .. import  schema,utils,outh2
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = APIRouter(tags=["Login"], prefix='/login')

@router.post("/",response_model=schema.Token)
async def loginForAccessToken(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await UserRepository.get_by_name(form_data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect username or password")
    if not utils.verify_password(form_data.password,user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=30) 
    access_token = outh2.create_access_token({"username":user.username,"site_id":user.site_id, "user_type":user.authorization},access_token_expires)
    return schema.Token(access_token=access_token,token_type="bearer")

@router.get("/me",response_model=schema.Token)
async def me(current_user : Annotated[schema.TokenData, Depends(outh2.get_current_user)],Authorization: Annotated [str ,Header()] ):
    return schema.Token(access_token=Authorization.split(' ')[1],token_type="bearer")

@router.post('/refresh')
async def refresh(Authorization: Annotated [str ,Header()] ):
    return schema.Token(access_token= await outh2.refreshToken(token=Authorization.split(' ')[1]),token_type="bearer")



