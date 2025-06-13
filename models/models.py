from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db_context

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    grant_lists = relationship("GrantList", back_populates="owner", cascade="all, delete-orphan")

# Pydantic models for request/response
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True

class GrantList(Base):
    __tablename__ = "grant_lists"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="grant_lists")
    grants = relationship("Grant", back_populates="grant_list")

class Grant(Base):
    __tablename__ = "grants"
    id = Column(Integer, primary_key=True)
    list_id = Column(Integer, ForeignKey("grant_lists.id"))
    title = Column(String)
    description = Column(String)
    link = Column(String)
    grant_list = relationship("GrantList", back_populates="grants")

class ProjectFormData(BaseModel):
    githubUrl: str = Field(..., description="Github Url of the project")
    title: str = Field(..., description="Title of the project")
    description: str = Field(..., description="Description of the project")

@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

with get_db_context() as db:
    # Do something with the database
    users = db.query(User).all()

