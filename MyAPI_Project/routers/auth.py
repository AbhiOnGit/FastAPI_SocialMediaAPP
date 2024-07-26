from typing import Optional, List
import sys
# fasapi dependency
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
router = APIRouter(prefix="/login")

from sqlalchemy.orm import Session

sys.path.insert(0, 'D:\\Python_API_VSCode\\MyAPI_Project')
from models import User
from schemas import UserLogin, Token
from database import get_db
from oauth2 import create_Token

# Method 1:
@router.post("/", response_model= Token)
def login(login_credential : UserLogin, db: Session= Depends(get_db)):     
    output = db.query(User).filter(User.email == login_credential.email).first()    
    if not output:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, 
                            detail = "Invalid credentials")    
    if login_credential.password != output.password:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, 
                            detail = "Invalid credentials")
    
    access_token = create_Token(login_credential.model_dump())
    return {"access_token": access_token, "token_type":"Bearer Token" }


# Method 2 : Use OAuth2PasswordRequestForm
# @router.post("/", response_model= Token)
# def login(login_credential : OAuth2PasswordRequestForm = Depends(), db: Session= Depends(get_db)):     
#     output = db.query(User).filter(User.email == login_credential.username).first() # Below line is same as this.    
#     if not output:
#         raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, 
#                             detail = "Invalid credentials")    
#     if login_credential.password != output.password:
#         raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, 
#                             detail = "Invalid credentials")
#     print(type(login_credential))
#     access_token = create_Token({"username": login_credential.username})
#     return {"access_token": access_token, "token_type":"Bearer Token" }
