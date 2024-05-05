from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel 

app = FastAPI()


class post(BaseModel):
    title: str
    content: str
    published:bool=True
    rating: Optional[int]=None


my_posts =[{"title":"title of post 1" , "content":"Contenet of post 1","id":1},
           {"title":"Favourite food" , "content":"Biryani ","id":2}
           ]

@app.get("/") 
def root():
    return {"message": "Welcome to my api!!!"}


@app.get("/posts")
def get_post():
    return {"data": "This is your post"}

@app.post("/posts")
def create_post(post:post):
    print(post)
    print(post.dict())
    return {"data":"post"}
