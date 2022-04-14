from fastapi import Body, FastAPI,Response, status,HTTPException,Depends,APIRouter
from typing import List,Optional
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import oauth2
from ..database import engine,get_db
from .. import models,schemas,oauth2

router=APIRouter(prefix='/posts',tags=['Posts'])



@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user),limit:int=5, skip:int=0,search:Optional[str]=""):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


# @app.get("/posts")
# async def get_posts():
#     cursor.execute("""SELECT * FROM posts """)
#     posts= cursor.fetchall()
#     return {"data": posts}

# @app.post("/posts",status_code=status.HTTP_201_CREATED)
# async def create_posts(post:Post):
#     cursor.execute("""INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING *""",(post.title,post.content,post.published) )
#     new_post = cursor.fetchone()
#     conn.commit()
#     return {"data":new_post}
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.CreatePost,db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    new_post=models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(current_user.email)
    return new_post


@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id==id).first()
    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
        response.status_code=status.HTTP_404_NOT_FOUND
        return {"message":f"post with id {id} not found"}
    return post




# @router.get("{id}")
# def get_post(id:int):
#     cursor.execute("""SELECT * FROM posts WHERE id=%s""",(str(id)) )
#     post = cursor.fetchone()
#     # post = find_post(id)
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
#         # response.status_code=status.HTTP_404_NOT_FOUND
#         # return {"message":f"post with id {id} not found"}
#     return {"data":post}

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

    
# @app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):
#     cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",(str(id)) )
#     deleted_post = cursor.fetchone()
#     conn.commit()
#     if deleted_post==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
#     # return {"message":f"Post of index {index} was successfully deleted"}
#     return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,updated_post:schemas.PostBase,db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested action")
     
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()
   

# @app.put("/posts/{id}")
# def update_post(id:int,post:Post):
#     cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.published,str(id)) )
#     updated_post=cursor.fetchone()
#     conn.commit()
#     if updated_post==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")
   
#     return {"data":updated_post}



