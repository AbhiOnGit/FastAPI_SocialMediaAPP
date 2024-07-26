from typing import Optional, List
import sys
# fasapi dependency
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
router = APIRouter(prefix="/users")


from sqlalchemy.orm import Session

sys.path.insert(0, 'D:\\Python_API_VSCode\\MyAPI_Project')
from models import User
from schemas import UserCreate, UserResponse
from database import get_db

# @app.get("/users", status_code = status.HTTP_201_CREATED, response_model=List[UserResponse])
@router.get("/", status_code = status.HTTP_201_CREATED, response_model=List[UserResponse])
def get_user(db: Session= Depends(get_db)):    
    output = db.query(User).all()     # 'User' is SQLAlchemy model defined in module "models"
    return output


# @app.post("/users", status_code = status.HTTP_201_CREATED, response_model=UserResponse)
@router.post("/", status_code = status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user : UserCreate, db: Session= Depends(get_db)):     
    new_user = User(**user.model_dump() )  
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
