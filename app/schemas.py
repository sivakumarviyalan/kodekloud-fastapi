from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr
from sqlmodel import Column, Field, Relationship, TIMESTAMP, text, SQLModel

class PostCreate(BaseModel):
    title: str
    content: str

class Posts(SQLModel, PostCreate, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    published: Optional[bool] = Field(nullable=False, default=True)
    created_at: Optional[datetime] = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")))
    owner_id: Optional[int] = Field(nullable=False, foreign_key="users.id", ondelete="CASCADE")
    owner: Optional["Users"] = Relationship(back_populates="posts")

class PostOut(BaseModel):
    Posts: Posts
    votes: int

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(nullable=False) 

class Users(SQLModel, UserCreate, table=True):
    email: EmailStr = Field(unique=True)
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str = Field(nullable=False)
    created_at: Optional[datetime] = Field(default=None, sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")))
    posts: list["Posts"] = Relationship(back_populates="owner")

class UserOut(BaseModel):
    email: EmailStr
    id: int
    created_at: Optional[datetime]

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Votes(SQLModel, table=True):
    user_id: int = Field(nullable=False, primary_key=True, foreign_key="users.id", ondelete="CASCADE")
    post_id: int = Field(nullable=False, primary_key=True, foreign_key="posts.id", ondelete="CASCADE")

class Vote(BaseModel):
    post_id: int
    dir: int

