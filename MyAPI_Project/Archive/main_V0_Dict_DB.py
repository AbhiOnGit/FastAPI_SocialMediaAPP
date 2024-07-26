from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
app = FastAPI()


class Post(BaseModel):   # Creating a model for request body
    title: str            
    content : str
    # id : str
    published : bool = True    #default is set to True, if user doesn't pass this tag in request body
    rating : Optional[int] = None  ##default is set to null, if user doesn't pass this tag in request body

# myresp = [{"title": "1", "content": "11", "id":"1"}, {"title": "2", "content": "12", "id":"2"}]
myresp = list() 


@app.post("/Posts", status_code = status.HTTP_201_CREATED)
def Posts(new_post : Post):           # new_post will be an object of class "Post"
   print(new_post.dict())             # To convert new_post (data received from frontend) to dictionary
   new_resp = new_post.dict()
   new_resp["id"] = randrange(0, 100)
   myresp.append(new_resp)
   return {"data" : new_resp}


@app.get("/Posts")
def Posts():
    return {"data": myresp}


@app.get("/")
async def root():
    return {"Author": "Abhishek", "Name":"Abhishek!!"}


def find_id(id):
    for data in myresp:
        if data["id"] == (id):
            print("Input->", data)
            return data
    return None


@app.get("/Posts/{id}")     #id is defined as a paramter.
def get_post(id:int, response : Response):
    resp = find_id(id)
    if resp == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"Give id '{id}' is not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message" : f"Give id '{id}' is not found"}
    return {"data": resp}


def find_delete_idx(id):
    for idx, data in enumerate(myresp):
        if data["id"] == (id):
            return idx
    


@app.delete("/Posts/{id}")     #id is defined as a paramter.
def delete_post(id:int, response : Response):
    idx = find_delete_idx(id)
    if idx != None:
        myresp.pop(idx)
        return {"detail": f"Given id '{id}' is successfully deleted."}
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"Given id '{id}' is not deleted")
        

@app.put("/Posts/{id}")
def update_post(id:int, new_post : Post):           # new_post will be an object of class "Post"
    idx = find_delete_idx(id)                       # Get the index for given id
    if idx == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                        detail = f"Give id '{id}' is not found")

    new_resp = new_post.dict()
    new_resp["id"] = id
    myresp[idx] = new_resp
    return {"data" : new_resp}

