from typing import Optional
from random import randrange

from pydantic import BaseModel

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
app = FastAPI()

import psycopg2
from psycopg2.extras import RealDictCursor

try:
    # conn = psycopg2.connect(host, database, user, password)
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
                            password='Abhikeerti', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Connect with data base is successful.")    
except:
    print("Connection failed")


class postBaseClass(BaseModel):   # Creating a model for request body
    id : Optional[int] = None
    title: str            
    content : str
    published : bool = False       #default is set to True, if user doesn't pass this tag in request body
    rating : Optional[int] = None  ##default is set to null, if user doesn't pass this tag in request body

myresp = list() 


@app.get("/")
async def root():
    cursor.execute("""select * from posts""")
    output = cursor.fetchall()    
    return {"data": output}


@app.get("/Posts")
def GET_method():
    cursor.execute("""select * from posts""")
    output = cursor.fetchall()    
    return {"data": output}


@app.get("/Posts/{id}")     #id is defined as a paramter.
def GETONE_method(id:int, response : Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # cursor.execute(f"SELECT * FROM posts WHERE id = {id}")
    output = cursor.fetchall()
    if not output:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"Given id '{id}' is not found")    
    return {"data": output}


@app.post("/Posts", status_code = status.HTTP_201_CREATED)
def POST_method(new_post : postBaseClass):  # new_post will be an object of class "postBaseClass"   
    new_rec = new_post.model_dump()       # To convert new_post (data received from frontend) to dictionary
    newId = randrange(0, 100)   
    cursor.execute("""INSERT INTO posts (id, title, content, published, rating) 
                  VALUES (%s, %s, %s, %s, %s) RETURNING * """,(newId, new_post.title, new_post.content, 
                                                  new_post.published, new_post.rating))
    output = cursor.fetchone()
    conn.commit()
    return {"message": output}


@app.delete("/Posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def DELETE_method(id:int, response : Response):
    # cursor.execute(f"DELETE FROM posts WHERE id = {id}")
    cursor.execute("""DELETE FROM posts WHERE id = %s returning * """, (str(id),))
    output = cursor.fetchone()
    if not output:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"Given id '{id}' is not found")        
    conn.commit()
     

@app.put("/Posts/{id}")
def PUT_method(id:int, update_post : postBaseClass):  
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s, rating = %s 
                   WHERE id = %s RETURNING * """,(update_post.title, update_post.content, 
                                                  update_post.published, update_post.rating, str(id)))
    
    output = cursor.fetchone()
    if not output:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"Given id '{id}' is not found")        
    conn.commit()
    return {"message": output}

