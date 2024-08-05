from typing import Optional, List
from random import randrange

# fasapi dependency
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Body
app = FastAPI()

#Postgress dependency
import psycopg2
from psycopg2.extras import RealDictCursor

#SQLAlchemy
from sqlalchemy.orm import Session
from database import Base, engine # import user defined Base, engine variables from module "database"
from database import get_db       # import user defined function get_db from module "database"
from schemas import postBaseClass # import user defined pydantic schema model from module "schemas"
from schemas import updateClass, updateResponse, UserCreate, UserResponse
import models                      # import user defined SQLAlchemy database model from module "models"
from routers import posts, users, auth, vote, post1


### CORS management
# origins = [*]
origins = [
    "https://www.google.com"
    # "https://localhost.tiangolo.com",
    # "http://localhost",
    # "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#IMP - Following line is responsible to create table in postgress database
models.Base.metadata.create_all(bind=engine)

app.include_router(post1.router)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return "Welcome Abhishek!"



