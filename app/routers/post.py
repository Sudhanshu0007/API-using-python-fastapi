from fastapi import FastAPI,Response,status,HTTPException,Depends ,APIRouter
from..database import engine,get_db
from sqlalchemy.orm import Session
from .. import models,schemas,oauth2
from typing import List

router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)


#<------------------------------------Retrive all Posts-------------------------------------->

@router.get("/",response_model=List[schemas.PostResponse])
def get_post(db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts=cursor.fetchall()

    posts=db.query(models.Post).all()
    return posts



#<------------------------------------Create a new Post-------------------------------------->

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_post(post:schemas.PostCreate ,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts(title,content,published) VALUES (%s,%s,%s) RETURNING * """,
    #                (post.title,post.content,post.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    print(current_user.email)
    new_post=models.Post(**post.model_dump())
    db.add(new_post)   
    db.commit() 
    db.refresh(new_post)
    return new_post



#<------------------------------------Retrive single Post by id-------------------------------------->

@router.get("/{id}",response_model=schemas.PostResponse)
def get_post(id:int,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id)))
    # post=cursor.fetchone()
    
    post=db.query(models.Post).filter(models.Post.id==id).first()    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} was not found')
    return post


#<------------------------------------Delete Post-------------------------------------->

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def deleted_post(id:int,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",(str(id),))
    # deleted_post=cursor.fetchone()
    # conn.commit()
    
    deleted_post=db.query(models.Post).filter(models.Post.id==id)
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id {id} does not exist')
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



#<------------------------------------Update Post-------------------------------------->

@router.put("/{id}",response_model=schemas.PostResponse)
def update_post(id: int,updated_post:schemas.PostCreate,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s , content =%s , published=%s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id)))
    # updated_post=cursor.fetchone()
    # conn.commit()
    
    post_query=db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'post with id {id} does not exist')
    
    post_query.update(updated_post.model_dump(),synchronize_session=False)
    db.commit()

    return post_query.first()