from fastapi import HTTPException, Depends, status, APIRouter
from sqlmodel import Session, select, func
from .. import schemas, oauth2
from ..database import get_session

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Posts)
def create_post(post: schemas.PostCreate, session: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user)) -> schemas.Posts:
    post = schemas.Posts(owner_id=current_user.id, **post.model_dump())
    session.add(post)
    session.commit()
    session.refresh(post)

    return post

@router.get("/", response_model= list[schemas.PostOut])
def read_posts(session: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user),
               limit: int = 20, skip: int = 0) -> list[schemas.PostOut]:
    results = session.exec(select(schemas.Posts, func.count(schemas.Votes.post_id).label("votes")).join(
        schemas.Votes, onclause=schemas.Votes.post_id==schemas.Posts.id, isouter=True).group_by(schemas.Posts.id).
        limit(limit).offset(skip)).all()
    
    return [{"Posts": post, "votes": votes} for post, votes in results]

@router.get("/{id}", response_model= list[schemas.PostOut])
def read_post(id: int, session: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user)) -> list[schemas.PostOut]:
    results = session.exec(select(schemas.Posts, func.count(schemas.Votes.post_id).label("votes")).join(
        schemas.Votes, onclause=schemas.Votes.post_id==schemas.Posts.id, isouter=True).group_by(schemas.Posts.id).
        filter(schemas.Posts.id==id)).all()

    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")

    return [{"Posts": post, "votes": votes} for post, votes in results]

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, session: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user)):
    post = session.get(schemas.Posts, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    session.delete(post)
    session.commit()

    return post

@router.put("/{id}")
def update_post(id: int, session: Session = Depends(get_session), current_user: int = Depends(oauth2.get_current_user)):
    post = session.get(schemas.Posts, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post.title = "Updated Title"
    post.content = "Updated Content"
    post.published = True

    session.add(post)
    session.commit()
    session.refresh(post)
    
    return post