"""Authentication routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

from .jwt import create_access_token, verify_password, get_password_hash

router = APIRouter(prefix="/auth", tags=["auth"])


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/register", response_model=Token)
async def register(user: UserCreate):
    """Register a new user."""
    # TODO: Check if user exists, create in DB
    hashed = get_password_hash(user.password)
    token = create_access_token(data={"sub": user.email})
    return Token(access_token=token)


@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    """Login and get access token."""
    # TODO: Verify credentials from DB
    token = create_access_token(data={"sub": user.email})
    return Token(access_token=token)
