from typing import Optional,List
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body 
from random import randrange
import psycopg2
import time
from sqlalchemy.orm import Session
from psycopg2.extras import RealDictCursor
from.import models,schemas,utils
from.database import engine,get_db
from.routers import post,user,auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI() 

# while True:
#     try:
#         conn=psycopg2.connect(host='localhost', database='fastapi',
#                           user='postgres',password='1234',cursor_factory=RealDictCursor)
#         cursor= conn.cursor()
#         print('connection succesfull')
#         break
#     except Exception as error:
#         print('Connection failed ')
#         print("Error %s"%error)
#         time.sleep(5)


# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# def find_index_post(id):
#     for i,p in enumerate(my_posts):
#         if p["id"]==id:
#             return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/") 
def root():
    return {"message": "Welcome to my api!!!"}
