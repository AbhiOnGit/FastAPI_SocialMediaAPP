from typing import Optional, List
import sys
# fasapi dependency
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
router = APIRouter()

from sqlalchemy.orm import Session
from sqlalchemy import func

sys.path.insert(0, 'D:\\Python_API_VSCode\\MyAPI_Project')
import models 
from schemas import postBaseClass, updateClass, updateResponse, postResponse
from database import get_db
import oauth2


# @app.get("/Posts", response_model=List[updateResponse])
# @router.get("/Posts", response_model=List[updateResponse])
@router.get("/Post1")
def GET_method(db: Session= Depends(get_db),
               user_emailId:int = Depends(oauth2.get_current_user) ):
    print("ABABABABABABABABABBABABABABA----")
    #Get all posts belong to user. 
    user = db.query(models.User).filter(models.User.email == user_emailId).first()  
    output = db.query(models.Post).filter(models.Post.user_id == user.id).all()   
    # print("XXXXXXXXXXXXXXXXXXXXXX", type(output), type(output[0]))
    # result = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes
    #                     , models.Post.id == models.Votes.post_id, 
    #                     isouter=True).group_by(models.Post.id).filter(models.Post.user_id == user.id).all
    print("XXXXXXXXXXXX", models.Post.user_id, user.id)
    result = db.query(models.Post,func.count(models.Votes.post_id)).add_columns(func.count(models.Votes.post_id)).join(models.Votes
                        , models.Post.id == models.Votes.post_id, 
                        isouter=True).group_by(models.Post.id).filter(models.Post.user_id == user.id).all()
    # temp = result[0][1]
    # print("ZZZZZZZZZZZZZZZZZZZZZZZZZZ",result[0], temp, type(temp))
    return output



# @app.get("/Posts/{id}")     #id is defined as a paramter.
@router.get("/Posts/{id}",  response_model=postBaseClass)     #id is defined as a paramter.
def GETONE_method(id:int, response : Response, db: Session= Depends(get_db), 
               user_emailId:int = Depends(oauth2.get_current_user)):
    
    output = db.query(models.Post).filter(models.Post.id == id).first() 
    if not output:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"Given id '{id}' is not found")  
      
    #Verify that the requested post belongs to same user. 
    user = db.query(models.User).filter(models.User.email == user_emailId).first()  
    if output.user_id != user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, 
                            detail = f"You are not authorized to view the post with id='{id}'.")
    
    return output


# @app.post("/Posts", status_code = status.HTTP_201_CREATED, response_model=updateResponse)
@router.post("/Posts", status_code = status.HTTP_201_CREATED, response_model=updateResponse)
def POST_method(new_post : postBaseClass, db: Session= Depends(get_db), 
                user_emailId:str = Depends(oauth2.get_current_user)):   
    # output = models.Post(title=new_post.title, content=new_post.content ) # Below line is same as this
    userId = db.query(models.User).filter(models.User.email == user_emailId).first()  
    output = models.Post(user_id = userId.id, **new_post.model_dump())  # '**' is used to unpack dictionary and create new object for class Post
    db.add(output)
    db.commit()
    db.refresh(output)
    return output


# @app.put("/Posts/{id}", response_model=updateResponse)
@router.put("/Posts/{id}", response_model=updateResponse)
def PUT_method(id:int, update_post : updateClass, db: Session= Depends(get_db), 
               user_emailId:int = Depends(oauth2.get_current_user)):     
    
    update_SQL = db.query(models.Post).filter(models.Post.id == id)
    output = update_SQL.first()
    if not output:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"Given id '{id}' is not found") 
    #Verify that the requested post for deletion belongs to same user. 
    user = db.query(models.User).filter(models.User.email == user_emailId).first()  
    if output.user_id != user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, 
                            detail = f"You are not authorized to update a post with id='{id}'.")
      
    update_SQL.update(update_post.model_dump())
    db.commit()
    return update_SQL.first()
    

# @app.delete("/Posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
@router.delete("/Posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def DELETE_method(id:int, response : Response, db: Session= Depends(get_db), 
               user_emailId:int = Depends(oauth2.get_current_user)):
    
    delete_post = db.query(models.Post).get(id)
    if not delete_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"Given id '{id}' is not found")     
     
    #Verify that the requested post for deletion belongs to same user. 
    user = db.query(models.User).filter(models.User.email == user_emailId).first()  
    if delete_post.user_id != user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, 
                            detail = f"You are not authorized to delete a post with id='{id}'.")
    
    db.delete(delete_post)
    db.commit()


@router.get("/search", response_model=List[updateResponse])
def GET_method(db: Session= Depends(get_db),
               user_emailId:int = Depends(oauth2.get_current_user),
               limit: int = 10, skip:int = 0, search : Optional[str] = "" ):
    print("XXXXXXXXXXXXXXXXXXXXXXX", limit, skip, search)
    #Get all posts belong to user. 
    output = db.query(models.Post).filter(models.Post.title.contains
                                          (search)).limit(limit).offset(skip).all()

    return output
