from fastapi import Body, FastAPI,Response, status,HTTPException,Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional,List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine,get_db
from sqlalchemy.orm import Session
from .routers import user,post,auth,vote


# models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello orldssadsa"}


while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='postgres',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('database connection was successful')
        break
    except Exception as error:
        print('connection to db failed')
        print('error was',error)
        time.sleep(2)
        

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(vote.router)

