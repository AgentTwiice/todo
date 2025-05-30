from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlmodel import Session, select

from .database import get_session
from .models import Calendar, User
from .utils import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth")


class UserIn(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str


@router.post("/register", response_model=Token)
def register(user_in: UserIn, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.email == user_in.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=user_in.email, hashed_password=hash_password(user_in.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    access = create_access_token({"sub": str(user.id)})
    refresh = create_access_token({"sub": str(user.id)}, expires_seconds=604800)
    return {"access_token": access, "refresh_token": refresh}


@router.post("/login", response_model=Token)
def login(user_in: UserIn, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == user_in.email)).first()
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access = create_access_token({"sub": str(user.id)})
    refresh = create_access_token({"sub": str(user.id)}, expires_seconds=604800)
    return {"access_token": access, "refresh_token": refresh}


@router.get("/google/callback", response_model=Token)
def google_callback(code: str, request: Request, session: Session = Depends(get_session)):
    user: User | None = getattr(request.state, "current_user", None)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    access = f"{code}_access"
    refresh = f"{code}_refresh"
    calendar = Calendar(user_id=user.id, provider="google", access_token=access, refresh_token=refresh)
    session.add(calendar)
    session.commit()
    return {"access_token": access, "refresh_token": refresh}
