from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func


router = APIRouter(
    prefix= "/posts",
    tags= ['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
def get_post(db: Session = Depends(get_db), current_user: int = Depends(
    oauth2.get_current_user), limit : int = 50 , skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    #SELECT posts.*,COUNT(votes.post_id) AS votes FROM posts LEFT JOIN votes ON posts.id = votes.post_id GROUP BY posts.id;
    post_results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id,
                                         isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    #to make get retrieve just authorized post:-
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return  post_results

@router.post("/",status_code= status.HTTP_201_CREATED, response_model= schemas.Post)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(
    oauth2.get_current_user
)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # # To push my changes to my database
    # conn.commit()

    #Notice => **post.dict() = to unpack all post shcema

    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(
    oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id)))
    # post = cursor.fetchone()
    #post = find_post(id)
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    #SELECT posts.*,COUNT(votes.post_id) AS votes FROM posts LEFT JOIN votes ON posts.id = votes.post_id GROUP BY posts.id;
    post_results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post_results:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"Post with id: {id} was not found")
       # response.status_code = status.HTTP_404_NOT_FOUND
       # return {"Message": f"Post with id: {id} is not found"}
    
    #to make get retrieve just authorized post:-
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
    #                         detail="Not authorized to perform requested action")
    
    return  post_results

@router.delete("/{id}",status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(
    oauth2.get_current_user
)):
    # we did not use f string format because we don't want to pass data directly to my SQL Query
    #cursor.execute(f"DELETE FROM posts WHERE id = {id}")
    # so we use this format
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(str(id),))
    # post = cursor.fetchone()

    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"Post with id: {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(
    oauth2.get_current_user
)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    query_post = db.query(models.Post).filter(models.Post.id == id)
    post2 = query_post.first()
    if post2 == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"Post with id: {id} does not exist")
    
    if post2.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    query_post.update(post.dict(), synchronize_session=False)
    db.commit()

    return  query_post.first()