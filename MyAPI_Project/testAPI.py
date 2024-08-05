from fastapi import FastAPI
from starlette.requests import Request
import asyncio
import time
import requests
from requests.auth import AuthBase

app  = FastAPI()

user = {
        "email": "test01@gmail.com",
        "password": "Abhipwd121212"
    }


class TokenAuth(AuthBase):
    """Implements a token authentication scheme."""

    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        """Attach an API token to the Authorization header."""
        request.headers["Authorization"] = f"Bearer {self.token}"
        return request

@app.get("/")
async def endpoint1():
    print("Hello1")
    # time.sleep(10)
    # await asyncio.sleep(10)
    req = requests.post('http://127.0.0.1:8000/login', json=user)
    token =  req.json()["access_token"]
    post_req = requests.get('http://127.0.0.1:8000/additionalInfo', auth=TokenAuth(token))
    return post_req.json()

# Multiple query paramter
# Sample URL: http://127.0.0.1:8001/query?qry=test1&qu=test2&security=false
@app.get("/query")
async def endpoint2(qry : str|None = None, qu : str|None = None, security: bool = False  ):  # To make a query paramter mandatory, Do not assign default value like None or some other value.
    print("Hello2", qry)
    print("Hello3", qu)
    print("Hello3", security)
    return {"query1" : qry, "query2" : qu, "security" : security}


# Multiple path and query parameters
@app.get("/item/{itemId}/user/{user_id}")
async def endpoint3(itemId : int, user_id : int|bool , qry : str|None = None,
                     qu : str|None = None, security: bool = False  ):
    print("Path paramter 1", itemId)
    print("Path paramter 2", user_id)
    print("Query1", qry)
    print("Query2", qu)
    print("Query3", security)
    return {"Path1" : itemId, "path2" : user_id,  "query1" : qry, "query2" : qu, "security" : security}


# Define path paramter using Enum (enumerations) - To explore further, try it using swagger.
from enum import Enum
class validItemName(str, Enum):
    val1 = "alexnet"
    val2 = "resnet"
    val3 = "lenet"

@app.get("/Enum/{itemName}")
async def endpoint4(itemName : validItemName):
    print(itemName)
    print(itemName.name)
    print(itemName.value)
    return {"Test" : "Passed"}


# Use of Annotated
from typing import Annotated
from fastapi import FastAPI, Query

@app.get("/annotated/")
async def endpoint5(q: Annotated[str | None, Query(max_length=5)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

