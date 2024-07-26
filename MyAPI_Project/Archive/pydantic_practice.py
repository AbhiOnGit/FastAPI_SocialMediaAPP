from fastapi import FastAPI, Response, status, HTTPException
from typing import Optional
from random import randrange
app = FastAPI()

from pydantic import BaseModel

class pydanticPost_Test(BaseModel):
    title:str
    content: str
    id : Optional[int] = None

temp_resp = [{"title": "Abhi", "content": "movie", "id": 55}, {"title": "Keerti", "content": "series", "id": 56}]

@app.get("/")
async def root():
    return {"data": temp_resp}

@app.post("/")
async def post_req(postReq : pydanticPost_Test):   #postReq is an object of 'Pydantic BaseModel class 
    print(postReq)                # Pydantic data         
    print(postReq.title)          # Read fields from Pydantic data 
    temp = postReq.model_dump()   # Convert Pydantic data to dictionary
    print(temp)                   # Read fields from dictionary
    print(temp["title"])
    return {"data" : postReq}


@app.post("/add")
async def post_req(postReq : pydanticPost_Test):    
    temp = postReq.model_dump()   
    temp["id"] = randrange(0, 100000)
    temp_resp.append(temp)
    return {"data" : temp_resp}


@app.get("/check/{id}")
async def getIdPost(id : int, response : Response):
    print(id)
    selectPost = findpost(id)
    if not selectPost:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found.") 
    return {"data": selectPost}

def findpost(id):
    for post in temp_resp:
        print(post["id"], id)
        print(type(post["id"]), type(id))
        # if str(post["id"]) == str(id):
        if post["id"] == id:
            print("found")
            return post
        
@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletepost(id : int):
    idx = findIndex(id)
    if not idx:
        print(temp_resp)
        temp_resp.pop(idx)
        print(temp_resp)
        
    
    
def findIndex(id):
    for idx, post in enumerate(temp_resp):
        if post["id"] == id:
            return idx
       

       
@app.put("/postUpdate/{id}")
def updatepost(id : int, post : pydanticPost_Test,):
    idx = findIndex(id)
    if idx == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found.") 
    post_dict = post.model_dump()
    orig_post = temp_resp[idx]
    orig_post["title"] = post_dict["title"]
    orig_post["content"] = post_dict["content"]
    return {"message" : "Post updated"}