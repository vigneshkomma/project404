from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timezone, timedelta
import uuid

from app.core.database import get_db
from app.models.user import User

router = APIRouter()

#Config
SECRET_KEY = "CHNAGE_THIS_TO_ENV_SWCRET"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24

pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")


#utils

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain,hashed):
    return pwd_context.verify(plain, hashed)

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)


#sign-up
@router.post("/signup")
def signup(email:str, password:str, username:str, db: Session = Depends(get_db)):
    user_exists = db.query(User).filter(User.email == email).first()

    if user_exists:
        raise HTTPException(status_code=400,detail="User alredy exists")
    
    new_user = User(
        id = str(uuid.uuid4()),
        email = email,
        username = username,
        password_hash = hash_password(password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"user_id":new_user.id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


#Login
@router.post("/login")
def login(email:str,password:str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"user_id":user.id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }



