from fastapi import HTTPException, Depends, status, APIRouter
from sqlmodel import Session
from .. import schemas, utils
from ..database import get_session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, session: Session = Depends(get_session)) -> schemas.UserOut:
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    db_user = schemas.Users(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, session: Session = Depends(get_session)) -> schemas.UserOut :
    user = session.get(schemas.Users, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not found")
    
    return user