from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, Token, UserResponse
from app.core.security import generate_password_hash, verify_password, create_access_token


router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(status_code = 400, detail = "A user with this email already exists.")
    
    hashed_password = generate_password_hash(user_in.password)
    new_user = User(email = user_in.email, hashed_password=hashed_password, full_name=user_in.full_name)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login", response_model=Token)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user:
        raise HTTPException(status_code = 401, detail = "Wrong email address or password.")
    
    if not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code = 401, detail = "Wrong email address or password.")
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

