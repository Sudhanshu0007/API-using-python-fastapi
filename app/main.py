from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel 
from random import randrange
import psycopg2
import time
from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published:bool=True
  

while True:
    try:
        conn=psycopg2.connect(host='localhost', database='fastapi',
                          user='postgres',password='1234',cursor_factory=RealDictCursor)
        cursor= conn.cursor()
        print('connection succesfull')
        break
    except Exception as error:
        print('Connection failed ')
        print("Error %s"%error)
        time.sleep(5)




my_posts =[{"title":"title of post 1" , "content":"Contenet of post 1","id":1},
           {"title":"Favourite food" , "content":"Biryani ","id":2}
           ]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p["id"]==id:
            return i

@app.get("/") 
def root():
    return {"message": "Welcome to my api!!!"}


@app.get("/posts")
def get_post():
    cursor.execute("""SELECT * FROM posts""")
    posts=cursor.fetchall()
    return {"data": posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
    cursor.execute("""INSERT INTO posts(title,content,published) VALUES (%s,%s,%s) RETURNING * """,
                   (post.title,post.content,post.published))
    new_post=cursor.fetchone()
    conn.commit()
    return {"data":new_post}

@app.get("/posts/{id}")
def get_post(id:int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id)))
    post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} was not found')
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"error":"Post Not Found"}
    return {"post_detail" : post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def deleted_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",(str(id),))
    deleted_post=cursor.fetchone()
    conn.commit()
    
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} does not exist')
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int,post:Post):
    cursor.execute("""UPDATE posts SET title=%s , content =%s , published=%s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id)))
    updated_post=cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id {id} does not exist')
    return {'data':updated_post}