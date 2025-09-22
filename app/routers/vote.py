from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session
from .. import schemas, database, oauth2

router = APIRouter(
    prefix="/vote",
    tags=["Votes"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, session: Session = Depends(database.get_session), current_user: int = Depends(oauth2.get_current_user)):
    post = session.get(schemas.Posts, vote.post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {vote.post_id} not found")

    existing_vote = session.get(schemas.Votes, (current_user.id, vote.post_id))
    if vote.dir == 1:
        if existing_vote:
            raise HTTPException(status_code=status. HTTP_409_CONFLICT, detail=f"{current_user.id} has already voted on post {vote.post_id}")
        new_vote = schemas.Votes(user_id=current_user.id, post_id=vote.post_id)
        session.add(new_vote)
        session.commit()
        session.refresh(new_vote)
        return {"message": "Successfully voted"}
    elif vote.dir == 0:
        if not existing_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found")
        session.delete(existing_vote)
        session.commit()
        return {"message": "Successfully removed vote"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid vote direction")