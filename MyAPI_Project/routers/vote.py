from typing import Optional, List
import sys
# fasapi dependency
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
router = APIRouter(prefix="/vote")
import oauth2
import models


from sqlalchemy.orm import Session

sys.path.insert(0, 'D:\\Python_API_VSCode\\MyAPI_Project')
from models import Votes
from schemas import votingData, votingDataResponse, voterOnPost
from database import get_db


@router.get("/", response_model=List[votingDataResponse])
def get_votes(db: Session= Depends(get_db)):    
    print("cdcdcdcd", id)    
    output = db.query(models.Votes).all()         
    return output

@router.get("/user", response_model=List[votingDataResponse])    #### Code needs to be updated to make it for specific user
def get_votes(db: Session= Depends(get_db)):        
    output = db.query(models.Votes).all()         
    return output

@router.get("/post/{id}", response_model=List[voterOnPost])            
def get_votes(id:int, db: Session= Depends(get_db)):            
    output = db.query(models.Votes).filter(models.Votes.post_id == id).all()        
    # print("anananna" , output[0].userInfo.email) 
    return output

@router.post("/", status_code = status.HTTP_201_CREATED)
def create_user(vote : votingData, db: Session= Depends(get_db),
                user_emailId:str = Depends(oauth2.get_current_user)): 

    post_exist = db.query(models.Post).filter(models.Post.id == vote.post_id).first() 

    if post_exist == None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail = f"Post {vote.post_id} does not exist.")

    user = db.query(models.User).filter(models.User.email == user_emailId).first()      
    found_vote = db.query(Votes).filter(Votes.user_id == user.id, Votes.post_id == vote.post_id).first()     

    if vote.dir == 1:
        if found_vote:            
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail = "Vote is already added by user.")
        else:            
            vote_req = Votes(post_id = vote.post_id, user_id = user.id )
            db.add(vote_req)
            db.commit()
            db.refresh(vote_req)
            return {"message": f"New vote is added for post {vote.post_id} by user {user.id}."}
    else:            
        if found_vote:
            db.delete(found_vote)
            db.commit()  
            return {"message": f"Vote is deleted from post {vote.post_id} by user {user.id}."}           
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail = "Vote does not exist.")
